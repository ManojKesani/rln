# S-001 Compose stack and health endpoint
Milestone: M0 Foundation
Status: todo   <!-- todo | doing | done -->
Depends on: -

## Goal
Start the whole stack with one command and confirm every service is alive.

## Done when (runnable in 2 minutes)
1. `make up` starts nginx, web, api, postgres, redis, phoenix, worker without errors.
2. `curl localhost/api/health` returns 200 with the contract JSON.
3. Phoenix loads at localhost:6006.
4. `docker compose down && make up` works with no manual steps.
5. Stop redis: /api/health returns 503 with redis "down".

## Backend tasks
- [ ] Run the API locally with no databases: expect 503, both services "down".
- [ ] Postgres service: pinned pgvector image, named volume, healthcheck.
- [ ] Redis service: pinned image, healthcheck.
- [ ] Phoenix service: pinned image, port 6006.
- [ ] API Dockerfile (uv install from uv.lock) and compose service with depends_on healthchecks. Hosts are `postgres` and `redis`, not localhost.
- [ ] Worker service: same image, placeholder command that stays alive.
- [ ] nginx.conf: / to web, /api to api, `proxy_buffering off` on /api.
- [ ] Makefile: up, down, logs, smoke (curl -fsS on health).

## Frontend tasks
- [ ] Static index.html saying "Trillian" and "mostly harmless", served by the web service. No fetch calls, no framework.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/config.py` | Reads env vars into one settings object | pydantic_settings.BaseSettings (uv add pydantic-settings) | Settings, settings |
| `apps/api/app/routers/health.py` | GET /api/health: pings postgres and redis, 200 or 503 | fastapi.APIRouter, fastapi.responses.JSONResponse, asyncpg, redis.asyncio.Redis, app.config.settings | router, check_postgres(), check_redis() |
| `apps/api/app/main.py` | Creates the FastAPI app and mounts routers | fastapi.FastAPI, app.routers.health.router | app |
| `apps/api/Dockerfile` | Builds the API image: uv install from uv.lock, run uvicorn | base python image, uv, pyproject.toml, uv.lock | image running app.main:app on 0.0.0.0:8000 |
| `docker-compose.yml` | Defines nginx, web, api, worker, postgres, redis, phoenix with healthchecks | .env, apps/api/Dockerfile, nginx/nginx.conf, web-placeholder/ | ports 80 (app) and 6006 (Phoenix) |
| `nginx/nginx.conf` | Routes / to web and /api to api, proxy_buffering off on /api | (none) | listens on 80 |
| `Makefile` | up, down, logs, smoke targets | docker compose, curl | make targets |
| `.env.example` | Documents every env var | (none) | DATABASE_URL, REDIS_URL, POSTGRES_*, PHOENIX_* |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `web-placeholder/index.html` | Static page: Trillian, mostly harmless. Served by the web service until S-007 | (none) | (none) |

## Contract
```
GET /api/health -> 200
{"status": "ok", "version": "0.1.0", "services": {"postgres": "ok", "redis": "ok"}}
503 if a dependency is down: same shape, status "degraded", that service "down".
```

## Out of scope
Login, tracing code, real features, any real frontend.

## Notes
Pin image versions, never use latest. All config via .env; commit .env.example. Open question: should /health check Phoenix? Default no.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
