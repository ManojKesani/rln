"""Request/response shapes for the chat routes, plus the SSE event payloads.

Changing a field here changes the API contract: run `make openapi` afterwards so
the frontend's generated types match. The SSE event models are NOT in openapi.json
(streams aren't described by it), so apps/web/src/lib/sse.ts mirrors them by hand.
"""
import uuid
from datetime import datetime

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    provider: str
    model: str
    title: str | None = None


class ConversationCreated(BaseModel):
    id: uuid.UUID


class ConversationOut(BaseModel):
    id: uuid.UUID
    title: str | None
    provider: str
    model: str
    updated_at: datetime


class MessageOut(BaseModel):
    role: str       # "user" | "assistant" | "system"
    content: str
    created_at: datetime | None = None   # the checkpointer doesn't store per-message times


class SendMessageIn(BaseModel):
    """Used by both /messages and /stream. provider/model are optional per-message overrides."""
    content: str
    provider: str | None = None
    model: str | None = None


class Usage(BaseModel):
    input: int
    output: int


class SendMessageOut(BaseModel):
    message: MessageOut
    usage: Usage


# --- SSE event payloads (the `data:` JSON of each event in services/streaming.py) ---

class TokenEvent(BaseModel):    # event: token
    delta: str


class UsageEvent(BaseModel):    # event: usage
    input: int
    output: int
    latency_ms: int


class ErrorEvent(BaseModel):    # event: error  (exception class name only)
    message: str
