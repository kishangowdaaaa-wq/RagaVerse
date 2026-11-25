
"""API endpoints for RagaVerse Carnatic music learning modules."""

from fastapi import APIRouter, HTTPException, Query

from app.knowledge import LEARNING_MODULES
from app.schemas.learning import (
    LearningModuleDetailResponse,
    LearningModuleListResponse,
)


router = APIRouter()


@router.get(
    "/",
    response_model=LearningModuleListResponse,
)
def get_learning_modules(
    level: str | None = Query(default=None),
    q: str | None = Query(default=None),
):
    """List learning modules with optional filters."""

    results = LEARNING_MODULES

    if level:
        term = level.casefold().strip()
        results = [
            module
            for module in results
            if module["level"].casefold() == term
        ]

    if q:
        term = q.casefold().strip()
        results = [
            module
            for module in results
            if term in module["title"].casefold()
            or term in module["description"].casefold()
            or any(
                term in lesson["title"].casefold()
                or term in lesson["summary"].casefold()
                for lesson in module["lessons"]
            )
        ]

    return {
        "count": len(results),
        "results": results,
    }


@router.get(
    "/{module_id}",
    response_model=LearningModuleDetailResponse,
)
def get_learning_module(module_id: str):
    """Retrieve a learning module and all its lessons."""

    for module in LEARNING_MODULES:
        if module["id"] == module_id:
            return module

    raise HTTPException(
        status_code=404,
        detail="Learning module not found.",
    )
