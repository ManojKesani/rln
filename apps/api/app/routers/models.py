"""GET /api/models: the providers and models the picker offers. Logic is in llm/catalog.py."""
from fastapi import APIRouter

from app.llm.catalog import list_all_providers
from app.schemas.models import ModelsResponse

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("", response_model=ModelsResponse)
async def get_models():
    return ModelsResponse(providers=await list_all_providers())
