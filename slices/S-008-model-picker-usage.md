# S-008 Model picker and usage logging
Milestone: M1 Chat with history and model selection
Status: todo   <!-- todo | doing | done -->
Depends on: S-007

## Goal
Choose provider and model per message and see what each reply used.

## Done when (runnable in 2 minutes)
1. Switching model mid-conversation uses the new model next turn.
2. Each call writes a row in llm_calls.
3. The badge matches llm_calls and the Phoenix trace.
4. The header shows total tokens for the conversation.

## Backend tasks
- [ ] llm_calls migration (provider, model, tokens, latency, trace_id).
- [ ] Callback handler that logs each call.
- [ ] Per-message provider and model override.
- [ ] Usage endpoint.

## Frontend tasks
- [ ] Provider and model dropdowns in the header (data from /api/models).
- [ ] Token badge under each reply and a conversation total.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0002_llm_calls.py` | Creates llm_calls table | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/llm_call.py` | llm_calls: provider, model, tokens, latency, trace_id, conversation_id | db.base | LlmCall |
| `apps/api/app/llm/callbacks.py` | Callback handler that writes an llm_calls row per call | langchain_core.callbacks.BaseCallbackHandler, db.session | UsageCallbackHandler |
| `apps/api/app/schemas/usage.py` | Response models | pydantic | CallUsage, ConversationUsage |
| `apps/api/app/services/usage.py` | Sums usage for a conversation | db.models.llm_call | get_conversation_usage(id) |
| `apps/api/app/services/chat.py (edit)` | Accept provider/model overrides, attach the callback | llm.callbacks | send_message |
| `apps/api/app/routers/conversations.py (edit)` | GET /{id}/usage | services.usage | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/ModelPicker.tsx` | Provider and model dropdowns | hooks.useModels | ModelPicker |
| `apps/web/src/components/TokenBadge.tsx` | Shows in/out tokens and latency under a reply | (props) | TokenBadge |
| `apps/web/src/api/hooks.ts (edit)` | Add useModels, useUsage | react-query | useModels, useUsage |
| `apps/web/src/pages/ChatPage.tsx (edit)` | Header with picker and total tokens | ModelPicker, TokenBadge | ChatPage |

## Contract
```
GET /api/conversations/{id}/usage -> {"input", "output", "calls": [{"provider", "model", "input", "output", "latency_ms", "trace_id"}]}
```

## Out of scope
Cost in money, rate limits, summarization.

## Log (fill in as you go)
- Built: llm_calls table (Alembic 0002), UsageCallbackHandler (async, one row per model call, own DB session, trace id from the current OTel span), per-message provider/model override on the stream endpoint (remembered on the conversation after a successful run), GET /api/conversations/{id}/usage, ModelPicker in the chat header, TokenBadge under replies, conversation token total in the header.
- Deviations from the contract: calls in /usage include an extra created_at; the S-007 sidebar selects were replaced by the header picker; the callback is also attached in the non-streaming send_message.
- How to test: alembic upgrade head, make openapi, switch fake to groq mid-conversation via curl or the UI, compare the badge, the llm_calls row, the /usage response and the Phoenix trace (search the trace_id).
- Known gaps: badges map the Nth assistant message to the Nth llm_calls row (older conversations and failed turns shift or lack badges); failed calls are not logged; one row per LLM call, so tool loops will give several rows per reply; trace_id is null outside a recording span; the override is saved only after a successful stream; output tokens include hidden reasoning tokens.
