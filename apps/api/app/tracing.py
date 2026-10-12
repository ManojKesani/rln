"""Sends traces to Phoenix. Three separate pieces cooperate:

  register()               (arize-phoenix-otel) creates an OpenTelemetry tracer provider
                           that exports spans to Phoenix, and makes it the global one.
  FastAPIInstrumentor      adds one HTTP span per request. register() alone does not.
  LangChainInstrumentor    turns LangChain/LangGraph runs (agent, model calls) into
                           spans nested under the HTTP span. It is also what puts
                           session.id (our thread_id) on the trace.

All of them share one trace per request, which is why the trace_id we store in
llm_calls (llm/callbacks.py) can be searched in Phoenix.
"""
import logging

from fastapi import FastAPI
from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from phoenix.otel import register

from app.config import settings

log = logging.getLogger(__name__)


def _provider():
    # OTLP/HTTP traces path on Phoenix. The host is the Compose service name, not localhost.
    endpoint = settings.phoenix_collector_endpoint.rstrip("/") + "/v1/traces"
    return register(
        project_name=settings.phoenix_project_name,  # the project you open in the Phoenix UI
        endpoint=endpoint,
        set_global_tracer_provider=True,
        # Explicit service name so it doesn't depend on OTEL_SERVICE_NAME being set.
        resource=Resource.create({"service.name": "trillian-api"}),
    )


def setup_tracing(app: FastAPI) -> None:
    """Called once from main.py."""
    provider = _provider()
    # /api/health is excluded so the Docker healthcheck doesn't flood Phoenix.
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider, excluded_urls="/api/health")
    LangChainInstrumentor().instrument(tracer_provider=provider)


def setup_script_tracing():
    """For standalone scripts (no FastAPI app): LangChain spans only.
    Returns the provider so the script can call force_flush() before it exits,
    otherwise the last spans may never be sent."""
    provider = _provider()
    LangChainInstrumentor().instrument(tracer_provider=provider)
    return provider
