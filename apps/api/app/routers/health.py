"""GET /api/health: is the stack alive? Public (no login) and untraced.

Used by `make smoke` and handy for debugging. It opens a fresh connection per
check instead of reusing the app's pool, so it tests "can I reach Postgres/Redis
from scratch", not "is the pool healthy". Each check has a short timeout so one
dead service can't hang the endpoint; both run in parallel.
Returns 200 if both are up, else 503 with the same JSON shape.
"""
import asyncio

import asyncpg
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from app.config import settings

router = APIRouter()
TIMEOUT = 2.0  # seconds


async def check_postgres() -> bool:
    try:
        # asyncpg takes the plain postgresql:// URL directly (no SQLAlchemy involved here).
        conn = await asyncpg.connect(settings.database_url, timeout=int(TIMEOUT))
        try:
            await asyncio.wait_for(conn.fetchval("SELECT 1"), TIMEOUT)
        finally:
            await conn.close()
        return True
    except Exception:
        return False  # any failure at all means "down"


async def check_redis() -> bool:
    clint = Redis.from_url(
        settings.redis_url,
        socket_connect_timeout=TIMEOUT,
        socket_timeout=TIMEOUT,
    )
    try:
        return bool(await asyncio.wait_for(clint.ping(), TIMEOUT))
    except Exception:
        return False
    finally:
        await clint.aclose()


@router.get("/api/health")
async def health() -> JSONResponse:
    pg_ok, redis_ok = await asyncio.gather(check_postgres(), check_redis())
    all_ok = pg_ok and redis_ok
    body = {
        "status": "ok" if all_ok else "degraded",
        "version": settings.app_version,
        "services": {
            "postgres": "ok" if pg_ok else "down",
            "redis": "ok" if redis_ok else "down",
        },
    }
    return JSONResponse(body, status_code=200 if all_ok else 503)
