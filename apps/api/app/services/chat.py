"""Conversation logic: create, list, read history, and the non-streaming send.

Two stores work together, and it helps to keep them apart in your head:
  - conversations table (our SQLAlchemy model): id, title, provider, model, times.
  - LangGraph checkpointer (Postgres, managed by LangGraph): the actual messages,
    keyed by thread_id == conversation id. We never write messages ourselves.

The exceptions below are raised here and turned into HTTP codes in
routers/conversations.py (_http). services/streaming.py reuses _get and _text.
"""
import uuid
from datetime import datetime, timezone

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.builder import build_agent
from app.db.models.conversation import Conversation
from app.llm.callbacks import UsageCallbackHandler
from app.llm.factory import ProviderUnavailableError, UnknownProviderError, build_chat_model
from app.schemas.chat import MessageOut, SendMessageOut, Usage


class ConversationNotFound(Exception):
    pass


class BadModel(ValueError):
    pass


class ProviderCallError(RuntimeError):
    pass


def _text(content) -> str:
    """Message content is a str, or a list of blocks (str or {"text": ...}). Flatten to text."""
    if isinstance(content, str):
        return content
    parts = [b.get("text", "") if isinstance(b, dict) else str(b) for b in content]
    return "".join(parts)


def _role(m) -> str | None:
    """LangChain message class -> the role names the UI uses."""
    if isinstance(m, HumanMessage):
        return "user"
    if isinstance(m, AIMessage):
        return "assistant"
    if isinstance(m, SystemMessage):
        return "system"
    return None  # tool messages etc. are not shown in the chat history


def _validate_model(provider: str, model: str) -> None:
    """Build the model once just to prove provider and key are usable.
    It does NOT check that `model` exists at the provider (known gap)."""
    try:
        build_chat_model(provider, model)
    except (UnknownProviderError, ProviderUnavailableError) as e:
        raise BadModel(str(e)) from e


async def _get(session: AsyncSession, conv_id: uuid.UUID) -> Conversation:
    conv = await session.get(Conversation, conv_id)  # primary-key lookup
    if conv is None:
        raise ConversationNotFound(str(conv_id))
    return conv


async def create_conversation(session: AsyncSession, provider: str, model: str,
                              title: str | None) -> Conversation:
    _validate_model(provider, model)
    conv = Conversation(provider=provider, model=model, title=title)
    session.add(conv)
    await session.commit()  # commit assigns the id/defaults; expire_on_commit=False keeps them readable
    return conv


async def list_conversations(session: AsyncSession) -> list[Conversation]:
    rows = await session.execute(select(Conversation).order_by(Conversation.updated_at.desc()))
    return list(rows.scalars())


async def get_messages(session: AsyncSession, checkpointer, conv_id: uuid.UUID) -> list[MessageOut]:
    await _get(session, conv_id)  # 404 if the conversation doesn't exist
    # aget_tuple returns the LATEST checkpoint for this thread, or None if nothing was ever sent.
    tup = await checkpointer.aget_tuple({"configurable": {"thread_id": str(conv_id)}})
    if tup is None:
        return []
    out = []
    # "messages" is the channel (state key) the agent appends to.
    for m in tup.checkpoint["channel_values"].get("messages", []):
        role = _role(m)
        text = _text(m.content)
        # Skip tool messages (no role) and AI messages with no text (e.g. a reply
        # that is only a tool call). This is also why the Nth-badge-to-Nth-message
        # mapping in the UI breaks once tools exist.
        if role and text:
            out.append(MessageOut(role=role, content=text))
    return out


async def send_message(session: AsyncSession, checkpointer, conv_id: uuid.UUID, content: str,
                       provider: str | None, model: str | None) -> SendMessageOut:
    """Non-streaming turn. Same shape as services/streaming.py, but it waits for the whole reply."""
    conv = await _get(session, conv_id)
    provider = provider or conv.provider  # per-message override wins, else what the chat remembers
    model = model or conv.model
    try:
        chat_model = build_chat_model(provider, model)
    except (UnknownProviderError, ProviderUnavailableError) as e:
        raise BadModel(str(e)) from e

    agent = build_agent(chat_model, checkpointer)
    config = {
        "configurable": {"thread_id": str(conv_id)},  # selects the history to load/save
        "metadata": {"thread_id": str(conv_id), "provider": provider, "model": model},  # Phoenix labels
        "callbacks": [UsageCallbackHandler(conv_id, provider, model)],  # writes llm_calls rows
    }
    try:
        # ainvoke runs the whole agent loop and returns the final state.
        result = await agent.ainvoke({"messages": [{"role": "user", "content": content}]}, config=config)
    except Exception as e:  # never leak provider bodies or keys
        raise ProviderCallError(type(e).__name__) from e

    # result["messages"] is the FULL history. Find this turn's AI messages:
    # everything after the last human message.
    msgs = result["messages"]
    last_human = max(i for i, m in enumerate(msgs) if isinstance(m, HumanMessage))
    new = [m for m in msgs[last_human + 1:] if isinstance(m, AIMessage)]
    usage = Usage(
        input=sum((m.usage_metadata or {}).get("input_tokens", 0) for m in new),
        output=sum((m.usage_metadata or {}).get("output_tokens", 0) for m in new),
    )
    reply = _text(new[-1].content) if new else ""

    # Remember the model used, set a title from the first message, bump updated_at.
    conv.provider, conv.model = provider, model
    if conv.title is None:
        conv.title = content[:50]
    conv.updated_at = datetime.now(timezone.utc)
    await session.commit()

    return SendMessageOut(message=MessageOut(role="assistant", content=reply), usage=usage)
