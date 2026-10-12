"""The `llm_calls` table: one row per model call, written by llm/callbacks.py.

One user turn is currently one row, but a turn with tools will produce several
(one per model call in the loop). There is no link to a specific message yet,
which is why the UI pairs the Nth assistant message with the Nth row (fragile).
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LlmCall(Base):
    __tablename__ = "llm_calls"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # SET NULL (not CASCADE): deleting a conversation keeps its usage rows for cost history.
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), index=True, nullable=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)   # includes hidden reasoning tokens
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    trace_id: Mapped[str | None] = mapped_column(String, nullable=True)  # search this in Phoenix
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
