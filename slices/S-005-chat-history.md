# S-005 Chat endpoint with persistent history
Milestone: M1 Chat with history and model selection
Status: todo   <!-- todo | doing | done -->
Depends on: S-004

## Goal
Create conversations, send messages, get replies, and keep history across an API restart.

## Done when (runnable in 2 minutes)
1. POST a message and get a reply with usage (non-streaming).
2. Restart the api container; GET messages still returns everything.
3. Two conversations stay separate.
4. The call is a trace in Phoenix with the thread id.

## Backend tasks
- [ ] Alembic init and the first migration: conversations (id, title, provider, model, created_at).
- [ ] Postgres checkpointer keyed by thread_id.
- [ ] Plain model call or create_agent with no tools.
- [ ] Conversation endpoints per the contract.

## Frontend tasks
- [ ] None in this slice.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic.ini + alembic/env.py` | Async Alembic setup pointing at DATABASE_URL | alembic, app.db.base.Base | (migration env) |
| `apps/api/alembic/versions/0001_conversations.py` | Creates conversations table | alembic.op, sqlalchemy | upgrade(), downgrade() |
| `apps/api/app/db/base.py` | Declarative base | sqlalchemy.orm.DeclarativeBase | Base |
| `apps/api/app/db/session.py` | Async engine and session factory | sqlalchemy.ext.asyncio, config.settings | engine, SessionLocal, get_session() |
| `apps/api/app/db/models/conversation.py` | Conversation table: id, title, provider, model, timestamps | sqlalchemy, db.base | Conversation |
| `apps/api/app/db/checkpointer.py` | Opens the Postgres checkpointer for LangGraph/LangChain agents | langgraph.checkpoint.postgres (async saver) | open_checkpointer() |
| `apps/api/app/agents/builder.py` | Builds an agent around a chat model and checkpointer | langchain agents.create_agent (verify name) | build_agent(chat_model, checkpointer, system_prompt, tools) |
| `apps/api/app/schemas/chat.py` | Request and response models | pydantic | ConversationCreate, ConversationOut, MessageOut, SendMessageIn, SendMessageOut, Usage |
| `apps/api/app/services/chat.py` | Create/list conversations, read messages, send a message | db.session, db.models.conversation, llm.factory, agents.builder | create_conversation, list_conversations, get_messages, send_message |
| `apps/api/app/routers/conversations.py` | Conversation and message endpoints | fastapi, services.chat, schemas.chat | router |
| `apps/api/app/main.py (edit)` | Lifespan opens and closes the checkpointer | db.checkpointer | app |

### Frontend
None in this slice.

## Contract
```
POST /api/conversations {"provider", "model", "title": null} -> 201 {"id"}
GET /api/conversations -> [{"id", "title", "provider", "model", "updated_at"}]
GET /api/conversations/{id}/messages -> [{"role", "content", "created_at"}]
POST /api/conversations/{id}/messages {"content", "provider"?, "model"?} -> {"message", "usage": {"input", "output"}}
```

## Out of scope
Streaming, tools, summarization.

## Notes
- Built: conversations table (Alembic 0001, plus updated_at), AsyncPostgresSaver opened in the app lifespan, tool-less create_agent per request, conversation and message endpoints (protected). History lives in the checkpointer, keyed by thread_id = conversation id. A conversation remembers its provider/model, and POST can override and update them.
- Deviations from the contract: message created_at is null (the checkpointer doesn't store it); updated_at added to the table; GET messages returns only user/assistant/system text; errors: 404 unknown conversation, 400 bad or unavailable provider, 502 provider failure; added sqlalchemy[asyncio] (greenlet) and the psycopg/langgraph-checkpoint-postgres packages.
- How to test: docker compose exec api alembic upgrade head, then the curl sequence (two conversations, restart, re-read). In Phoenix, the CHAIN span has session.id = conversation id.
- Known gaps: no message timestamps; one checkpointer connection; agent rebuilt per request; migrations run by hand; usage output tokens include reasoning tokens.


## Log (fill in as you go)
- Built: conversations table (Alembic 0001, plus updated_at), AsyncPostgresSaver opened in the app lifespan, tool-less create_agent per request, conversation and message endpoints (protected). History lives in the checkpointer, keyed by thread_id = conversation id. A conversation remembers its provider/model, and POST can override and update them.
- Deviations from the contract: message created_at is null (the checkpointer doesn't store it); updated_at added to the table; GET messages returns only user/assistant/system text; errors: 404 unknown conversation, 400 bad or unavailable provider, 502 provider failure; added sqlalchemy[asyncio] (greenlet) and the psycopg/langgraph-checkpoint-postgres packages.
- How to test: docker compose exec api alembic upgrade head, then the curl sequence (two conversations, restart, re-read). In Phoenix, the CHAIN span has session.id = conversation id.
- Known gaps: no message timestamps; one checkpointer connection; agent rebuilt per request; migrations run by hand; usage output tokens include reasoning tokens.