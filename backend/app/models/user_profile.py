from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    experience_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="beginner",
    )

    musical_background: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    primary_instrument: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    years_of_experience: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    preferred_learning_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="beginner",
    )

    favorite_ragas: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    musical_goals: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="profile",
    )
