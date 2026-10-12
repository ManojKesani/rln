"""Login logic: check the password, create and read the session token (JWT).

Flow:
  POST /api/auth/login -> verify_credentials() -> create_access_token() -> cookie
  every later request  -> deps.require_user    -> decode_access_token()

There is no user table: the one username and its bcrypt hash come from .env.
The JWT is signed (not encrypted) with JWT_SECRET; anyone with the secret can
mint a valid cookie, so keep it private. Logout only deletes the cookie; the
token itself stays valid until it expires (known gap).
"""
import asyncio
import hmac
import logging
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import settings

log = logging.getLogger(__name__)
ALGORITHM = "HS256"


def _check_password(password: str, hashed: str) -> bool:
    try:
        # bcrypt only uses the first 72 bytes; newer bcrypt versions raise on longer input.
        return bcrypt.checkpw(password.encode()[:72], hashed.encode())
    except ValueError:
        # Typical cause: the hash in .env lost its single quotes and Compose mangled the $ signs.
        log.error("AUTH_PASSWORD_HASH is not a valid bcrypt hash (check the single quotes in .env)")
        return False


async def verify_credentials(username: str, password: str) -> bool:
    # compare_digest takes the same time however many characters match (no timing leak).
    user_ok = hmac.compare_digest(username.encode(), settings.auth_username.encode())
    # bcrypt is deliberately slow and CPU-bound, so run it in a thread to keep the event loop free.
    # It always runs, even for a wrong username, so response time doesn't reveal which part failed.
    pw_ok = await asyncio.to_thread(_check_password, password, settings.auth_password_hash)
    return user_ok and pw_ok


def create_access_token(username: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(hours=settings.token_ttl_hours)
    # "sub" (subject) = who this token is for; "exp" = expiry, enforced automatically on decode.
    return jwt.encode({"sub": username, "exp": exp}, settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """Username if the token is valid and unexpired, else None."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError:  # bad signature, expired, malformed...
        return None
    return payload.get("sub")
