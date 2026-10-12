# DEVLOG

Newest entries at the bottom. Each entry: what was built, decisions, surprises, and what to remember.

## S-001 Compose stack and health endpoint (tag s-001)

**Built:** Compose stack with nginx, web (static placeholder), api (FastAPI), worker (placeholder `sleep infinity`), postgres (pgvector 0.8.0-pg17), redis 7.4, phoenix 20.19.0. `GET /api/health` pings postgres and redis, returns 200 or 503 with the contract shape. Makefile: up, down, logs, smoke.

**Decisions**
- nginx is published on host port **8080**, not 80, because Caddy already uses 80. All checks and `make smoke` hit `localhost:8080/api/...`.
- Image versions are pinned, never `latest`.
- Dockerfile uses uv with `--frozen`, so after any `uv add` the image must be rebuilt (`docker compose build api`). The worker shares the image.
- Hosts inside Compose are service names (`postgres`, `redis`, `phoenix`), not localhost.

**Notes**
- A 502 from nginx right after `make up` or a rebuild usually means the api is still starting, or nginx holds the old container address. Wait a few seconds or `docker compose restart nginx`.
- `.env` is never committed. `.env.example` holds placeholders only (replace the real Postgres password there).

## S-002 Single-user login (tag s-002)

**Built:** `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`. bcrypt hash and username from `.env`, PyJWT HS256 token in an httpOnly, SameSite=Lax cookie (7 days). `require_user` dependency in `deps.py`. `scripts/hash_password.py` prints the hash line.

**Decisions**
- Env vars: `AUTH_USERNAME`, `AUTH_PASSWORD_HASH`, `JWT_SECRET`, `COOKIE_NAME`, `COOKIE_SECURE` (default false), `TOKEN_TTL_HOURS` (default 168).
- API refuses to start if the username, hash or secret is missing.
- Public routes: `/api/health`, `/api/auth/login`, `/api/auth/logout`. Every later router is mounted with `dependencies=[Depends(require_user)]` in `main.py`, so none can be forgotten.
- bcrypt runs in a thread and always runs, even for a wrong username, so timing doesn't leak which part failed.

**Notes**
- The bcrypt hash in `.env` **must be single-quoted** (`AUTH_PASSWORD_HASH='$2b$12$...'`). Compose treats `$` as a variable, and an unquoted hash makes every login return 401.
- `jar.txt` (curl cookie jar) holds a live session. Keep it in `.gitignore`.
- Known gaps: no CSRF token, no login rate limiting, logout doesn't revoke the JWT.

## S-003 Phoenix tracing (tag s-003)

**Built:** `tracing.py` registers a Phoenix tracer provider (project `trillian`) and instruments FastAPI, excluding `/api/health`. Dev-only `GET /api/debug/trace` (behind login) creates a child span and returns the trace id.

**Decisions**
- Added `opentelemetry-instrumentation-fastapi`. `register()` alone doesn't create HTTP spans.
- `setup_tracing(app)` takes the app as an argument.
- Service name is set explicitly with `resource=Resource.create({"service.name": "trillian-api"})`, so `OTEL_SERVICE_NAME` is redundant.
- OTLP endpoint is `http://phoenix:6006/v1/traces`.

**Notes**
- Phoenix's span panel doesn't show resource attributes. The service name was verified by printing `provider.resource.attributes`.
- `log.info` lines from app code are invisible in `docker compose logs` because the root logger defaults to WARNING. Use `print(..., flush=True)` for one-off checks, or add `logging.basicConfig(level=logging.INFO)` in `main.py`.
- Worker is not traced.

## S-004 Model factory and model list (tag s-004)

**Built:** Provider table (Groq, OpenRouter, NVIDIA NIM via `ChatOpenAI` with `base_url`; fake via `GenericFakeChatModel`), `build_chat_model(provider, model, **params)` with optional `rpm` rate limiter and `max_retries=0`, cached async `GET /api/models` (10 min cache, 5 s timeout, errors never cached), LangChain instrumentor, `scripts/compare_providers.py`.

**Decisions**
- A provider with no key is `available: false` with no network call. A provider with a key but a failed fetch is `available: true, models: [], error: "HTTP 401"` (extra `error` field beyond the contract; error text never includes keys).
- `max_retries=0` so that later retry middleware owns retries and every attempt shows as its own span.
- `./scripts` is bind-mounted read-only into the api container (it is outside the build context). Run scripts with `docker compose exec api python /app/scripts/compare_providers.py`.
- `setup_script_tracing()` added so standalone scripts get LangChain spans too.
- Dependencies kept small: `langchain-openai`, `httpx`, `openinference-instrumentation-langchain`. The old project's extras (`arize-phoenix` server package, native Groq/Google/Mistral/Ollama packages, MCP adapters, psycopg, sqlglot, python-dotenv) were deliberately not carried over.

**Notes**
- Verified: Groq (real models, real usage), fake (zero tokens, no network). **Not tested:** OpenRouter and NVIDIA (no keys).
- Groq's list includes non-chat models (Orpheus TTS, Prompt Guard). OpenRouter is huge. Filtering waits for capability flags.
- Default model ids in the compare script can go stale. Override with `--model provider=id` using ids from `/api/models`.
- `register()` in scripts uses SimpleSpanProcessor (warning is harmless). Consider batching for the API later.

## S-005 Chat endpoint with persistent history (tag s-005)

**Built:** `conversations` table (Alembic 0001, plus an extra `updated_at`), `AsyncPostgresSaver` opened in the app lifespan, tool-less `create_agent` built per request, endpoints to create/list conversations, read messages and send a message (non-streaming, returns reply and usage). A conversation remembers its provider/model, and POST can override and update them. Title defaults to the first 50 characters of the first message.

**Decisions**
- History lives in the checkpointer, keyed by `thread_id` = conversation id. Our `conversations` table points to it.
- Two Postgres drivers on purpose: SQLAlchemy uses asyncpg (URL rewritten to `postgresql+asyncpg://` in `session.py`), the checkpointer uses psycopg with the plain `postgresql://` URL.
- Migrations are run by hand: `docker compose exec api alembic upgrade head` (after any new migration or a fresh volume). Dockerfile copies `alembic.ini` and `alembic/`.
- Errors: 404 unknown conversation, 400 unknown or unavailable provider, 502 provider failure (exception class only).

**Notes**
- `sqlalchemy[asyncio]` is required. A plain `sqlalchemy` install crashes at import with a greenlet error.
- Phoenix `session.id` appears automatically on the CHAIN span from `config["configurable"]["thread_id"]` plus `metadata.thread_id`. No custom code needed.
- Hidden reasoning tokens (`gpt-oss-120b`: 44 and 47) are included in output tokens, so short replies can still cost a lot.
- History is resent every turn (input tokens went 83 to 106). Cost grows with conversation length, which is why summarization comes later.
- Messages have no timestamps (`created_at` is null), because the checkpointer doesn't store them. If S-007's UI needs times, add a `messages` table or use checkpoint metadata.
- Known gaps: one shared checkpointer connection, agent rebuilt per request, migrations manual.

## Cross-cutting reminders

- After any `uv add`: rebuild the image (`docker compose build api && make up`).
- Never commit `.env` or `jar.txt`. Check `git status` before every commit.
- Paste commands one at a time. Several terminal pastes got mangled (doubled `curl -s -b`, `docker compose docker compose`, lost YAML/Python indentation in chat).
- Verify library and API names against current docs. Unverified so far: base URLs for OpenRouter and NVIDIA, default model ids in the compare script.
- For S-006 (streaming): the usage sum and the "find new AI messages" logic in `send_message` will need to move into a callback or the final stream event.

## S-006 SSE streaming with usage event (tag s-006)

**Built:** `POST /api/conversations/{id}/stream` returning `text/event-stream`, with events `token`, `usage`, `done` and `error`.

**Decisions**
- Used `stream_mode="messages"` for per-token output. `updates` yields whole steps and `values` yields full state each step, so neither gives token granularity. Only `messages` was tried.
- Usage is read from the checkpointer after the stream ends and summed over the turn's AI messages. Groq returned real counts (84 in, 56 out), so `stream_usage=True` wasn't needed.
- 404 and 400 are real HTTP errors raised before the stream starts. Failures after it starts become an `error` event with the exception class only.
- Headers `Cache-Control: no-cache` and `X-Accel-Buffering: no` keep buffering off even if the nginx config changes.

**Notes**
- Verified through nginx on port 8080: tokens, then `usage`, then `done`. The fake model streams word by word with zero usage.
- Groq's deltas include two trailing spaces and a newline per line (markdown line breaks). The S-007 UI should render markdown or use `white-space: pre-wrap`.
- A failed turn leaves the user's message in the checkpointer history.

DEVLOG additions
react-router-dom chosen for routing (per frontend-rules).
openapi-typescript peers on TypeScript 5 while the Vite template ships 6, so legacy-peer-deps=true in apps/web/.npmrc (must be committed and copied in the Dockerfile).
TypeScript 6: baseUrl is deprecated (use paths alone), and erasableSyntaxOnly forbids constructor(public x).
Run frontend commands in apps/web, backend and Docker commands at the repo root. Running npx tsc outside apps/web offers to install an unrelated tsc package.
make openapi regenerates schema.d.ts after any backend contract change.


## S-008 Model picker and usage logging (tag s-008)

**Built:** `llm_calls` table, a LangChain async callback that writes a row per model call, per-message provider/model override, `GET /api/conversations/{id}/usage`, header model picker, token badges and a conversation total.

**Decisions**
- The callback opens its own short DB session per row, so logging never shares or blocks the request session, and a logging failure never breaks the chat.
- `trace_id` is read from the current OpenTelemetry span inside the callback. Verified: the id stored in `llm_calls` was found in Phoenix, and its tokens matched.
- Live badge uses the `usage` SSE event. Saved history uses `/usage`, with the Nth assistant message mapped to the Nth call.

**Notes**
- The fake model has `usage_metadata: null`, so it logs zeros.
- `gpt-oss-120b` reported 60 reasoning tokens inside 73 output tokens, so visible text is a small share of the output count.
- After backend contract changes, run `make openapi` before `npx tsc -b`.