"""Async database access for OUR tables (conversations, llm_calls).

Two Postgres drivers are in use on purpose:
  - SQLAlchemy + asyncpg (this file): our own tables.
  - psycopg (db/checkpointer.py): LangGraph's checkpointer, which needs it.
Both connect to the same database.

SessionLocal() makes a session; get_session() is the FastAPI dependency that
gives each request its own session and closes it afterwards. The usage callback
calls SessionLocal() directly to get an independent session.
"""
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


def async_url(url: str) -> str:
    # .env has a plain postgresql:// URL. SQLAlchemy needs the driver named explicitly.
    return url.replace("postgresql://", "postgresql+asyncpg://", 1)


# pool_pre_ping checks a pooled connection is alive before using it (survives DB restarts).
engine = create_async_engine(async_url(settings.database_url), pool_pre_ping=True)
# expire_on_commit=False: objects stay readable after commit() without a new query,
# which routers rely on (e.g. reading conv.id after create_conversation).
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session  # the request runs here; the session closes when it finishes
