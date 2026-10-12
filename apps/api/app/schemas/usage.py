"""Response shapes for GET /api/conversations/{id}/usage (built from llm_calls rows)."""
from datetime import datetime

from pydantic import BaseModel


class CallUsage(BaseModel):
    """One model call."""
    provider: str
    model: str
    input: int
    output: int
    latency_ms: int
    trace_id: str | None = None   # paste into Phoenix search to open the trace
    created_at: datetime


class ConversationUsage(BaseModel):
    """Totals plus every call, oldest first."""
    input: int
    output: int
    calls: list[CallUsage]
