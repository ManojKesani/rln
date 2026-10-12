# S-002 Single-user login
Milestone: M0 Foundation
Status: todo   <!-- todo | doing | done -->
Depends on: S-001

## Goal
Log in with env-configured credentials and stay logged in.

## Done when (runnable in 2 minutes)
1. Wrong password returns 401.
2. Right password returns 200 and sets an httpOnly cookie.
3. GET /api/auth/me returns the username with the cookie and 401 without.
4. Logout clears the cookie.

## Backend tasks
- [ ] Hashed password and username from .env.
- [ ] Auth router: login, logout, me.
- [ ] JWT in an httpOnly, SameSite cookie.
- [ ] Dependency that protects every /api route except /health and /auth/login.

## Frontend tasks
- [ ] None. The login page arrives in S-007.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/config.py (edit)` | Add auth settings: username, password hash, JWT secret, cookie name | pydantic_settings | Settings.auth_* |
| `apps/api/app/schemas/auth.py` | Request and response models | pydantic.BaseModel | LoginRequest, MeResponse |
| `apps/api/app/services/auth.py` | Check credentials, make and read JWTs | bcrypt, jwt (PyJWT), app.config.settings | verify_credentials(u, p), create_access_token(u), decode_access_token(t) |
| `apps/api/app/deps.py` | FastAPI dependency that rejects requests without a valid cookie | fastapi.Cookie, HTTPException, services.auth.decode_access_token | require_user |
| `apps/api/app/routers/auth.py` | POST /api/auth/login, POST /logout, GET /me | fastapi.APIRouter, Response, Depends, schemas.auth, services.auth, deps.require_user | router |
| `apps/api/app/main.py (edit)` | Mount auth router; protect later routers with require_user | routers.auth, deps | app |
| `scripts/hash_password.py` | Prints a bcrypt hash to paste into .env | bcrypt | (script) |

### Frontend
None in this slice.

## Contract
```
POST /api/auth/login {username, password} -> 200 {"ok": true} + Set-Cookie; 401 {"detail": "invalid credentials"}
POST /api/auth/logout -> 200 {"ok": true}
GET /api/auth/me -> 200 {"username": "..."} | 401
```

## Out of scope
Registration, roles, OAuth, password reset.

## Notes
Test everything with curl or /docs.

## Log (fill in as you go)
- Built: POST /api/auth/login, POST /api/auth/logout, GET /api/auth/me. Credentials from .env (bcrypt hash, constant-time username compare, bcrypt run in a thread). PyJWT HS256 token in an httpOnly, SameSite=Lax cookie (7 days). `require_user` dependency in deps.py; later routers get it via `include_router(..., dependencies=[Depends(require_user)])`. `scripts/hash_password.py` prints the hash line for .env.
- Deviations from the contract: none. Env var names are AUTH_USERNAME, AUTH_PASSWORD_HASH, JWT_SECRET, COOKIE_NAME, COOKIE_SECURE (default false), TOKEN_TTL_HOURS (default 168). Public routes: /api/health, /api/auth/login, /api/auth/logout. Added `uv add bcrypt pyjwt`, so the api image needs a rebuild. Compose host port is 8080, so checks hit localhost:8080/api.
- How to test: with B=localhost:8080/api
  1. Wrong password: curl -i -X POST $B/auth/login -H 'content-type: application/json' -d '{"username":"admin","password":"wrong"}' -> 401 {"detail":"invalid credentials"}
  2. Right password: same call with -c jar.txt -> 200 + Set-Cookie ... HttpOnly
  3. curl -i -b jar.txt $B/auth/me -> 200 {"username":"admin"}; without the cookie -> 401
  4. curl -i -b jar.txt -c jar.txt -X POST $B/auth/logout, then /auth/me again -> 401
- Known gaps: no CSRF token (SameSite=Lax only); no login rate limiting; logout only clears the cookie and does not revoke the JWT; API refuses to start if AUTH_USERNAME, AUTH_PASSWORD_HASH or JWT_SECRET is missing; jar.txt must stay out of git.
