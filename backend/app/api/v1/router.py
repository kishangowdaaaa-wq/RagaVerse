
from fastapi import APIRouter

from app.api.v1.endpoints import (
    audio,
    auth,
    conversations,
    health,
    knowledge,
    learning,
    profiles,
    ragas,
    users,
)

api_router = APIRouter()

api_router.include_router(health.router)

api_router.include_router(
    users.router,
    prefix="/users",
)

api_router.include_router(
    profiles.router,
    prefix="/users",
    tags=["Musician Profiles"],
)

api_router.include_router(
    auth.router,
    prefix="/auth",
)

api_router.include_router(
    conversations.router,
    prefix="/conversations",
)

api_router.include_router(
    ragas.router,
    prefix="/ragas",
)

api_router.include_router(
    knowledge.router,
    prefix="/knowledge",
)

api_router.include_router(
    learning.router,
    prefix="/learning",
)

api_router.include_router(
    audio.router,
    prefix="/audio",
    tags=["Audio Intelligence"],
)
