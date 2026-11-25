
"""Pydantic schemas for RagaVerse learning modules."""

from pydantic import BaseModel, ConfigDict, Field


class LearningLesson(BaseModel):
    """A single lesson within a learning module."""

    id: str
    title: str
    summary: str
    duration_minutes: int = Field(ge=1)


class LearningModule(BaseModel):
    """A structured Carnatic music learning module."""

    id: str
    title: str
    level: str
    description: str
    prerequisites: list[str] = Field(default_factory=list)
    lessons: list[LearningLesson] = Field(default_factory=list)


class LearningModuleListResponse(BaseModel):
    """Response containing available learning modules."""

    count: int
    results: list[LearningModule]


class LearningModuleDetailResponse(LearningModule):
    """Detailed learning module response."""

    model_config = ConfigDict(from_attributes=True)
