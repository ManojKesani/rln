"""Login, logout and "who am I". Flow: see services/auth.py.

The token travels in an httpOnly cookie, so browser JavaScript can't read it
(protects against token theft via XSS). Because the UI and API are served from
the same origin through nginx, the browser attaches the cookie automatically.
"""
from fastapi import APIRouter, Depends, HTTPException, Response

from app.config import settings
from app.deps import require_user
from app.schemas.auth import LoginRequest, MeResponse
from app.services.auth import create_access_token, verify_credentials

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
async def login(body: LoginRequest, response: Response):
    if not await verify_credentials(body.username, body.password):
        # Same message for wrong user and wrong password, on purpose.
        raise HTTPException(status_code=401, detail="invalid credentials")
    response.set_cookie(
        key=settings.cookie_name,
        value=create_access_token(body.username),
        max_age=settings.token_ttl_hours * 3600,
        httponly=True,                # not readable from JS
        samesite="lax",               # not sent on cross-site POSTs (our only CSRF defence for now)
        secure=settings.cookie_secure,  # True once served over HTTPS
        path="/",
    )
    return {"ok": True}


@router.post("/logout")
async def logout(response: Response):
    # Only clears the cookie in this browser; the JWT itself is not revoked.
    response.delete_cookie(settings.cookie_name, path="/")
    return {"ok": True}


@router.get("/me", response_model=MeResponse)
async def me(username: str = Depends(require_user)):
    # The frontend's RequireAuth calls this: 200 means logged in, 401 means go to /login.
    return MeResponse(username=username)
