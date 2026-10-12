"""HTTP layer for conversations: create, list, read messages, send, stream, usage.

Routers are deliberately thin (see ARCHITECTURE.md): parse the request, call a
service, translate domain exceptions into HTTP status codes, return a schema.
The real logic lives in services/chat.py, services/streaming.py, services/usage.py.

Auth: main.py mounts this router with dependencies=[Depends(require_user)], so
every route below needs a valid login cookie without repeating it per route.

Where the chat path starts:
    browser -> nginx -> POST /api/conversations/{id}/stream  (the `stream` route below)
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.chat import (ConversationCreate, ConversationCreated, ConversationOut, MessageOut,
                              SendMessageIn, SendMessageOut)
from app.schemas.usage import ConversationUsage
from app.services import chat, streaming
from app.services import usage as usage_service

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


def _http(e: Exception) -> HTTPException:
    """Map a domain exception (defined in services/chat.py) to an HTTP error.

    Services raise plain Python exceptions and know nothing about HTTP; this is
    the one place where they become status codes.
    """
    if isinstance(e, chat.ConversationNotFound):
        return HTTPException(404, "conversation not found")
    if isinstance(e, chat.BadModel):          # unknown provider, or provider has no API key
        return HTTPException(400, str(e))
    if isinstance(e, chat.ProviderCallError):  # the provider itself failed (class name only, no body)
        return HTTPException(502, f"provider call failed: {e}")
    raise e  # anything unexpected stays a 500 so we notice it


@router.post("", status_code=201, response_model=ConversationCreated)
async def create(body: ConversationCreate, session: AsyncSession = Depends(get_session)):
    # `session` is one DB session per request, opened by get_session() in db/session.py.
    try:
        conv = await chat.create_conversation(session, body.provider, body.model, body.title)
    except chat.BadModel as e:
        raise _http(e)
    return ConversationCreated(id=conv.id)


@router.get("", response_model=list[ConversationOut])
async def list_(session: AsyncSession = Depends(get_session)):
    rows = await chat.list_conversations(session)  # newest activity first
    return [ConversationOut(id=c.id, title=c.title, provider=c.provider, model=c.model,
                            updated_at=c.updated_at) for c in rows]


@router.get("/{conv_id}/messages", response_model=list[MessageOut])
async def messages(conv_id: uuid.UUID, request: Request, session: AsyncSession = Depends(get_session)):
    # Message history is NOT in our tables. It lives in the LangGraph checkpointer,
    # which main.py's lifespan stored on app.state at startup.
    try:
        return await chat.get_messages(session, request.app.state.checkpointer, conv_id)
    except chat.ConversationNotFound as e:
        raise _http(e)


@router.post("/{conv_id}/messages", response_model=SendMessageOut)
async def send(conv_id: uuid.UUID, body: SendMessageIn, request: Request,
               session: AsyncSession = Depends(get_session)):
    """Non-streaming chat turn: waits for the whole reply. Kept for curl and tests;
    the UI uses /stream below."""
    try:
        return await chat.send_message(session, request.app.state.checkpointer, conv_id,
                                       body.content, body.provider, body.model)
    except (chat.ConversationNotFound, chat.BadModel, chat.ProviderCallError) as e:
        raise _http(e)


@router.post("/{conv_id}/stream")
async def stream(conv_id: uuid.UUID, body: SendMessageIn, request: Request,
                 session: AsyncSession = Depends(get_session)):
    """Streaming chat turn (this is what the UI calls). Two phases, on purpose:

    1. prepare(): runs BEFORE the response starts, so a bad conversation id (404)
       or bad provider (400) is still a real HTTP error the client can see.
    2. stream_reply(): an async generator. StreamingResponse sends HTTP 200
       immediately, then forwards each string the generator yields. After this
       point a failure can no longer change the status code, so stream_reply
       reports it as an `error` event instead.
    """
    try:
        conv, chat_model = await streaming.prepare(session, conv_id, body.provider, body.model)
    except (chat.ConversationNotFound, chat.BadModel) as e:
        raise _http(e)
    gen = streaming.stream_reply(session, request.app.state.checkpointer, conv, chat_model, body.content)
    return StreamingResponse(
        gen,
        media_type="text/event-stream",
        # no-cache: don't let anything store the stream.
        # X-Accel-Buffering: tell nginx not to buffer, or tokens would arrive in one lump.
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/{conv_id}/usage", response_model=ConversationUsage)
async def usage(conv_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    # Reads our llm_calls table (written by llm/callbacks.py), not the checkpointer.
    try:
        return await usage_service.get_conversation_usage(session, conv_id)
    except chat.ConversationNotFound as e:
        raise _http(e)
