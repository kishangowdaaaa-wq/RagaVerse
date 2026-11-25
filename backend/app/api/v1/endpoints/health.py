from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Check application health",
)
async def health_check() -> HealthResponse:
    """
    Check whether the RagaVerse API is running.
    """

    settings = get_settings()

    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
    )