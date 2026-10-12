"""Response shapes for GET /api/models (what the model picker shows)."""
from pydantic import BaseModel


class ModelInfo(BaseModel):
    id: str     # what you pass back to the provider as `model`
    name: str


class ProviderInfo(BaseModel):
    name: str
    available: bool                # False when no API key is set (no network call is made)
    models: list[ModelInfo]
    error: str | None = None       # key present but the list fetch failed, e.g. "HTTP 401"


class ModelsResponse(BaseModel):
    providers: list[ProviderInfo]
