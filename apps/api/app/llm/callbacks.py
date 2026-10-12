"""Writes one llm_calls row for every model call. This is how usage is logged.

LangChain calls the methods below automatically because the handler is passed in
config["callbacks"] (see services/streaming.py). The callbacks reach child runs
too, so tool loops will log every model call they make.

Order of events for one call:
    on_chat_model_start(run_id=X)   -> remember start time and trace id
    ... model runs ...
    on_llm_end(run_id=X)            -> compute latency, read tokens, write a row

run_id is unique per model call, which is why the two dicts are keyed by it.

Design choices:
  - The row is written in its OWN short DB session, so logging never shares or
    blocks the request's session.
  - A logging failure is caught and logged, never raised: logging must not break chat.
Known gaps: there is no on_llm_error, so failed calls are not logged and their
entries stay in the two dicts (a small leak for the handler's lifetime, which is
one request).
"""
import logging
import time
import uuid

from langchain_core.callbacks import AsyncCallbackHandler
from opentelemetry import trace

from app.db.models.llm_call import LlmCall
from app.db.session import SessionLocal

log = logging.getLogger(__name__)


class UsageCallbackHandler(AsyncCallbackHandler):
    """One instance per request; knows which conversation and model it is logging for."""

    def __init__(self, conversation_id: uuid.UUID, provider: str, model: str):
        self.conversation_id = conversation_id
        self.provider = provider
        self.model = model
        self._started: dict[uuid.UUID, float] = {}          # run_id -> start time
        self._trace_id: dict[uuid.UUID, str | None] = {}    # run_id -> Phoenix/OTel trace id

    @staticmethod
    def _current_trace_id() -> str | None:
        """The OpenTelemetry trace we are inside right now, as 32 hex chars (what Phoenix shows).
        This lets a llm_calls row be matched to its trace. None if no span is recording."""
        ctx = trace.get_current_span().get_span_context()
        return format(ctx.trace_id, "032x") if ctx.is_valid else None

    async def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):
        # Chat models trigger this (not on_llm_start). Capture start time and trace id here.
        self._started[run_id] = time.perf_counter()
        self._trace_id[run_id] = self._current_trace_id()

    async def on_llm_end(self, response, *, run_id, **kwargs):
        t0 = self._started.pop(run_id, None)
        trace_id = self._trace_id.pop(run_id, None)
        latency = int((time.perf_counter() - t0) * 1000) if t0 else 0
        usage = {}
        try:
            # response.generations[0][0] is the first candidate of the first prompt.
            # usage_metadata is None for the fake model, hence `or {}`.
            usage = response.generations[0][0].message.usage_metadata or {}
        except (IndexError, AttributeError):
            pass
        try:
            async with SessionLocal() as s:
                s.add(LlmCall(
                    conversation_id=self.conversation_id, provider=self.provider, model=self.model,
                    # output_tokens includes hidden reasoning tokens for reasoning models.
                    input_tokens=usage.get("input_tokens", 0), output_tokens=usage.get("output_tokens", 0),
                    latency_ms=latency, trace_id=trace_id))
                await s.commit()
        except Exception:
            log.exception("could not write llm_calls row")  # never break the chat for logging
