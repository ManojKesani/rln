"""Runs one chat turn and turns it into Server-Sent Events (SSE).

Flow for POST /api/conversations/{id}/stream (see routers/conversations.py):

    prepare()       load the conversation, build the chat model   (can fail -> 404/400)
    stream_reply()  build agent -> agent.astream() -> yield events

Event order on success:  token, token, ... -> usage -> done
Event order on failure:  token, ... -> error   (HTTP status is already 200 by then)

An SSE message is plain text: "event: <name>\ndata: <json>\n\n". The browser side
parses it in apps/web/src/lib/sse.ts.
"""
import json
import time
import uuid
from collections.abc import AsyncIterator
from datetime import datetime, timezone

from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.builder import build_agent
from app.llm.callbacks import UsageCallbackHandler
from app.llm.factory import ProviderUnavailableError, UnknownProviderError, build_chat_model
from app.schemas.chat import ErrorEvent, TokenEvent, UsageEvent
from app.services.chat import BadModel, _get, _text


def sse(event: str, data: dict) -> str:
    """Format one SSE message. The blank line at the end is what ends the message."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def prepare(session: AsyncSession, conv_id: uuid.UUID,
                  provider: str | None = None, model: str | None = None):
    """Everything that can fail BEFORE streaming starts, so failures are real HTTP errors."""
    conv = await _get(session, conv_id)  # raises ConversationNotFound -> 404
    # A per-message override wins; otherwise use what the conversation remembers.
    provider = provider or conv.provider
    model = model or conv.model
    try:
        chat_model = build_chat_model(provider, model)
    except (UnknownProviderError, ProviderUnavailableError) as e:
        raise BadModel(str(e)) from e  # -> 400
    # Changed on the in-memory object only. It is saved by session.commit() at the
    # end of stream_reply, so a failed turn does NOT change the remembered model.
    conv.provider, conv.model = provider, model
    return conv, chat_model


async def stream_reply(session: AsyncSession, checkpointer, conv, chat_model,
                       content: str) -> AsyncIterator[str]:
    """Async generator: yields SSE strings that StreamingResponse sends as they appear."""
    conv_id = str(conv.id)

    # Built per request. That's fine because the agent holds no state: history
    # lives in the checkpointer (Postgres), keyed by thread_id.
    agent = build_agent(chat_model, checkpointer)

    config = {
        # Which conversation's history to load and save. Phoenix also shows this
        # as session.id on the trace.
        "configurable": {"thread_id": conv_id},
        # Tracing labels only: they show up on the Phoenix span, no behavior change.
        "metadata": {"thread_id": conv_id, "provider": conv.provider, "model": conv.model},
        # Called by LangChain on every model call; writes one llm_calls row each
        # (see llm/callbacks.py).
        "callbacks": [UsageCallbackHandler(conv.id, conv.provider, conv.model)],
    }
    t0 = time.perf_counter()
    try:
        # stream_mode="messages" yields (message_chunk, metadata) pairs, one per
        # token. We pass only the NEW user message: LangGraph loads the earlier
        # ones from the checkpointer, appends this one, runs the model, and saves
        # the result back when the run finishes.
        async for chunk, _meta in agent.astream(
            {"messages": [{"role": "user", "content": content}]},
            config=config,
            stream_mode="messages",
        ):
            # The stream can contain other message types (human, tool); only AI text goes to the UI.
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                # content is a plain string for most providers, or a list of
                # blocks ({"type": "text", "text": ...}) for some.
                text = chunk.content if isinstance(chunk.content, str) else "".join(
                    b.get("text", "") for b in chunk.content if isinstance(b, dict))
                if text:
                    yield sse("token", TokenEvent(delta=text).model_dump())

        # The stream is over, so the checkpointer holds the finished turn. Re-read
        # it and sum the AI messages that come after the last human message.
        # NOTE (fragile): this is separate from the llm_calls rows, and with tools
        # one turn will contain several AI messages. S-008 badges have the same
        # weakness. Linking llm_calls to message ids would remove both problems.
        tup = await checkpointer.aget_tuple({"configurable": {"thread_id": conv_id}})
        msgs = tup.checkpoint["channel_values"].get("messages", []) if tup else []
        last_human = max((i for i, m in enumerate(msgs) if isinstance(m, HumanMessage)), default=-1)
        new = [m for m in msgs[last_human + 1:] if isinstance(m, AIMessage)]
        usage = UsageEvent(
            # usage_metadata is None for the fake model, hence `or {}`.
            input=sum((m.usage_metadata or {}).get("input_tokens", 0) for m in new),
            output=sum((m.usage_metadata or {}).get("output_tokens", 0) for m in new),
            latency_ms=int((time.perf_counter() - t0) * 1000),
        )

        # Only on success: title from the first message, bump updated_at (sidebar
        # ordering), and persist the provider/model that prepare() set in memory.
        if conv.title is None:
            conv.title = content[:50]
        conv.updated_at = datetime.now(timezone.utc)
        await session.commit()

        yield sse("usage", usage.model_dump())
        yield sse("done", {})
    except Exception as e:
        # Never send provider error bodies to the client (they can echo keys).
        # Known gap: the user's message stays in the checkpointer history even
        # when the turn failed.
        yield sse("error", ErrorEvent(message=type(e).__name__).model_dump())
