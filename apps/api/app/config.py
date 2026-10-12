"""All configuration, read once from environment variables into `settings`.

In Docker the variables come from .env via `env_file:` in docker-compose.yml; the
`env_file=".env"` below only matters when you run the API outside Docker.
pydantic-settings matches env vars to field names case-insensitively
(auth_username <- AUTH_USERNAME).

A field WITHOUT a default is required: if it is missing, creating `Settings()`
raises at import time and the API refuses to start. That is deliberate for the
login settings, so you never run with auth silently misconfigured.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # ignore POSTGRES_* etc.

    app_env: str = "dev"          # "dev" also mounts /api/debug/*
    app_version: str = "0.1.0"

    # Plain postgresql:// URL. asyncpg (health check) and psycopg (checkpointer) use it
    # as is; db/session.py rewrites it for SQLAlchemy's asyncpg driver.
    database_url: str = "postgresql://trillian:change-me@postgres:5432/trillian"
    redis_url: str = "redis://redis:6379/0"

    # Login (single user). No defaults on the first three: the API fails fast if missing.
    auth_username: str
    auth_password_hash: str   # bcrypt hash; must be single-quoted in .env because it contains $
    jwt_secret: str           # signs the session cookie; changing it logs everyone out
    cookie_name: str = "trillian_session"
    cookie_secure: bool = False   # True only when served over HTTPS
    token_ttl_hours: int = 168    # 7 days

    # Tracing: where Phoenix listens inside the Compose network, and the project name shown in its UI.
    phoenix_collector_endpoint: str = "http://phoenix:6006"
    phoenix_project_name: str = "trillian"

    # Provider keys. Empty means "provider unavailable" (see llm/providers.py).
    groq_api_key: str = ""
    openrouter_api_key: str = ""
    nvidia_api_key: str = ""
    models_cache_ttl_s: int = 600          # how long GET /api/models results are cached
    models_fetch_timeout_s: float = 5.0    # per-provider timeout when listing models


settings = Settings()
