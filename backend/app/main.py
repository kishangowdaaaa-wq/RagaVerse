
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1.router import api_router
from app.core.config import get_settings


settings = get_settings()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "An intelligent AI-powered Carnatic music "
        "companion for musicians, students, teachers "
        "and music researchers."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register rate limiting
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
    ],
)

# API routes
app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to RagaVerse!",
        "description": (
            "Your Intelligent Carnatic Music Companion."
        ),
        "status": "running",
    }
