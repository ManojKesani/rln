"""Reads llm_calls rows for one conversation and totals them.

Written by llm/callbacks.py, read here, shown by the frontend's TokenBadge and
the header total. The totals are summed in Python from the same rows, so they
always agree with the per-call list.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.llm_call import LlmCall
from app.schemas.usage import CallUsage, ConversationUsage
from app.services.chat import _get


async def get_conversation_usage(session: AsyncSession, conv_id: uuid.UUID) -> ConversationUsage:
    await _get(session, conv_id)  # 404 if unknown
    rows = (await session.execute(
        select(LlmCall).where(LlmCall.conversation_id == conv_id).order_by(LlmCall.created_at)
    )).scalars().all()
    calls = [CallUsage(provider=r.provider, model=r.model, input=r.input_tokens, output=r.output_tokens,
                       latency_ms=r.latency_ms, trace_id=r.trace_id, created_at=r.created_at) for r in rows]
    return ConversationUsage(input=sum(c.input for c in calls), output=sum(c.output for c in calls), calls=calls)
