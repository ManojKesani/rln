"""App entry point: builds the FastAPI app, wires tracing, and mounts the routers.

Started by the Dockerfile as `uvicorn app.main:app`. Importing this module runs
config.py first (so a missing AUTH_* / JWT_SECRET env var stops the API here,
at startup, instead of on the first login).
"""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.config import settings
from app.db.checkpointer import open_checkpointer
from app.deps import require_user
from app.routers import auth, conversations, health, models
from app.tracing import setup_tracing


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Code before `yield` runs once at startup, code after it at shutdown.

    The checkpointer holds a Postgres connection, so it is opened once here and
    kept for the life of the process. Routes reach it via request.app.state.checkpointer.
    (Known gap: one shared connection for all requests.)
    """
    async with open_checkpointer() as checkpointer:
        app.state.checkpointer = checkpointer
        yield


app = FastAPI(title="Trillian API", version=settings.app_version, lifespan=lifespan)

# Runs once at import: registers the Phoenix exporter, then instruments FastAPI
# (one HTTP span per request) and LangChain (spans for model/agent runs).
setup_tracing(app)

# Public: no login needed.
app.include_router(health.router)
app.include_router(auth.router)  # login/logout are public; /me protects itself

# Protected: dependencies=[...] runs require_user before EVERY route in the router,
# so a new router can't accidentally be left open as long as it is mounted here.
app.include_router(models.router, dependencies=[Depends(require_user)])
app.include_router(conversations.router, dependencies=[Depends(require_user)])

if settings.app_env == "dev":
    from app.routers import debug  # imported lazily so it doesn't exist outside dev
    app.include_router(debug.router, dependencies=[Depends(require_user)])
