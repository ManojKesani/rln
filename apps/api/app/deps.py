"""FastAPI dependency that protects routes: no valid login cookie, no access.

Used two ways:
  - mounted on whole routers in main.py: include_router(..., dependencies=[Depends(require_user)])
  - as a parameter, when the route wants the username (see routers/auth.py: /me)
"""
from fastapi import HTTPException, Request

from app.config import settings
from app.services.auth import decode_access_token


async def require_user(request: Request) -> str:
    """Return the logged-in username, or raise 401."""
    token = request.cookies.get(settings.cookie_name)  # httpOnly cookie set by /api/auth/login
    username = decode_access_token(token) if token else None  # None if bad signature or expired
    if username is None:
        raise HTTPException(status_code=401, detail="not authenticated")
    return username
