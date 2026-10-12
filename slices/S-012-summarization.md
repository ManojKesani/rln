# S-012 Summarization and token ceiling
Milestone: M2 Agents, tools, token control
Status: todo   <!-- todo | doing | done -->
Depends on: S-011

## Goal
Keep long chats under a token budget and show where tokens go.

## Done when (runnable in 2 minutes)
1. A scripted 30-turn chat stays under the ceiling.
2. Context breakdown shows system prompt, summary, recent messages, tool output.
3. Old turns are summarized, recent turns stay verbatim.
4. Record tokens saved with and without.

## Backend tasks
- [ ] Summarization middleware or equivalent.
- [ ] Per-conversation ceiling setting.
- [ ] Context breakdown endpoint.
- [ ] The 30-turn test script.

## Frontend tasks
- [ ] Context breakdown panel in the chat.
- [ ] Warning when near the ceiling.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0006_token_ceiling.py` | conversations.token_ceiling | alembic | upgrade(), downgrade() |
| `apps/api/app/services/summarize.py` | Summarize old turns when over the ceiling | llm.factory, services.usage | maybe_summarize(conversation_id) |
| `apps/api/app/services/context.py` | Breaks the context into prompt, summary, recent, tool output | services.chat | context_breakdown(conversation_id) |
| `apps/api/app/agents/builder.py (edit)` | Add summarization middleware or equivalent | langchain middleware (verify) | build_agent |
| `apps/api/app/routers/conversations.py (edit)` | GET /{id}/context | services.context | router |
| `scripts/long_chat.py` | Scripted 30-turn chat logging tokens per turn | httpx | (script) |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/ContextPanel.tsx` | Bars for each context part | hooks.useContext | ContextPanel |
| `apps/web/src/pages/ChatPage.tsx (edit)` | Warning near the ceiling | ContextPanel | ChatPage |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Long-term memory.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
