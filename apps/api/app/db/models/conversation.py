"""The `conversations` table. It holds metadata only (title, which model, times).
The messages themselves live in the LangGraph checkpointer under thread_id = id."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)  # set from the first message
    # The provider/model last used; the picker shows these when you reopen the chat.
    provider: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # Not auto-updated by the database: services set it explicitly after each successful turn.
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
