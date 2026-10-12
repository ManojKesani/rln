"""Lists the models each provider offers, for GET /api/models (the model picker).

Rules:
  - fake: always available, one hard-coded model, no network.
  - no API key: available=False, no network call at all.
  - key but the fetch fails: available=True, models=[], error="HTTP 401" etc.
    (error text never includes keys)
  - success: cached in memory for models_cache_ttl_s; failures are never cached,
    so a temporary outage heals itself on the next request.
Known gaps: the lists include non-chat models (TTS, guard models) and OpenRouter's
list is huge; filtering waits for capability flags (S-013).
"""
import asyncio
import time

import httpx

from app.config import settings
from app.llm.providers import FAKE_MODEL_ID, PROVIDERS, ProviderConfig
from app.schemas.models import ModelInfo, ProviderInfo

# provider name -> (time cached, result). Lives in this process only; resets on restart.
_cache: dict[str, tuple[float, ProviderInfo]] = {}


async def _fetch(client: httpx.AsyncClient, p: ProviderConfig) -> ProviderInfo:
    if p.name == "fake":
        return ProviderInfo(name="fake", available=True,
                            models=[ModelInfo(id=FAKE_MODEL_ID, name="Fake (no network, zero tokens)")])
    if not p.available:
        return ProviderInfo(name=p.name, available=False, models=[])

    hit = _cache.get(p.name)
    if hit and time.monotonic() - hit[0] < settings.models_cache_ttl_s:  # monotonic: immune to clock changes
        return hit[1]

    try:
        r = await client.get(p.models_url, headers={"Authorization": f"Bearer {p.api_key}"})
        r.raise_for_status()  # turns 4xx/5xx into HTTPStatusError
        items = r.json().get("data", [])  # OpenAI-style list: {"data": [{"id": ...}, ...]}
        models = sorted((ModelInfo(id=i["id"], name=i.get("name") or i["id"]) for i in items),
                        key=lambda m: m.id)
        info = ProviderInfo(name=p.name, available=True, models=models)
        _cache[p.name] = (time.monotonic(), info)   # errors are never cached
        return info
    except httpx.HTTPStatusError as e:
        err = f"HTTP {e.response.status_code}"
    except httpx.HTTPError as e:
        err = type(e).__name__  # timeout, connection error, ...
    return ProviderInfo(name=p.name, available=True, models=[], error=err)


async def list_all_providers() -> list[ProviderInfo]:
    # One client for all; gather() fetches every provider in parallel so the slowest
    # one (bounded by the timeout) sets the total time, not the sum.
    async with httpx.AsyncClient(timeout=settings.models_fetch_timeout_s) as client:
        return list(await asyncio.gather(*(_fetch(client, p) for p in PROVIDERS.values())))
