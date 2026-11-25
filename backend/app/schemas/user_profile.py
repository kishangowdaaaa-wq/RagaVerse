
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ExperienceLevel = Literal[
    "beginner",
    "intermediate",
    "advanced",
]


class UserProfileUpdate(BaseModel):
    experience_level: ExperienceLevel = "beginner"

    musical_background: str | None = Field(
        default=None,
        max_length=5000,
    )

    primary_instrument: str | None = Field(
        default=None,
        max_length=100,
    )

    years_of_experience: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    preferred_learning_level: ExperienceLevel = "beginner"

    favorite_ragas: list[str] = Field(
        default_factory=list,
        max_length=50,
    )

    musical_goals: list[str] = Field(
        default_factory=list,
        max_length=20,
    )


class UserProfileResponse(BaseModel):
    user_id: int
    experience_level: ExperienceLevel
    musical_background: str | None
    primary_instrument: str | None
    years_of_experience: int | None
    preferred_learning_level: ExperienceLevel
    favorite_ragas: list[str]
    musical_goals: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
