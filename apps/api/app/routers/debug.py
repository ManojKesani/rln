"""Dev-only (see main.py): creates a span and returns its trace id.

A quick way to check the Phoenix wiring end to end: call it, then search the
returned trace_id in Phoenix (project "trillian"). You should see the HTTP span
from FastAPIInstrumentor with the "debug.trace" span nested inside it.
"""
from fastapi import APIRouter
from opentelemetry import trace

router = APIRouter(prefix="/api/debug", tags=["debug"])
tracer = trace.get_tracer("trillian.debug")


@router.get("/trace")
async def debug_trace():
    # start_as_current_span makes this the active span; its parent is the HTTP span.
    with tracer.start_as_current_span("debug.trace") as span:
        trace_id = format(span.get_span_context().trace_id, "032x")  # 32 hex chars, as Phoenix shows
    return {"trace_id": trace_id}
