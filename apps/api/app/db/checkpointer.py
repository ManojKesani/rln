"""Opens LangGraph's Postgres checkpointer: the store for chat history.

After each agent run LangGraph saves the full state (including the messages list)
as a "checkpoint" under a thread_id; before the next run it loads the latest one.
That is why we only send the NEW user message per turn. We use thread_id = the
conversation's id, so deleting or listing history is always per conversation.

The saver creates and manages its own tables (checkpoints, checkpoint_writes, ...),
separate from the SQLAlchemy models and Alembic migrations.
"""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.config import settings


@asynccontextmanager
async def open_checkpointer() -> AsyncIterator[AsyncPostgresSaver]:
    """Used by main.py's lifespan: the connection stays open until shutdown."""
    # The saver uses psycopg and wants the plain postgresql:// URL (no +asyncpg).
    async with AsyncPostgresSaver.from_conn_string(settings.database_url) as saver:
        await saver.setup()  # creates its own tables if missing; safe to run every startup
        yield saver
