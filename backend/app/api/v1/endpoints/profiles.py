
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import (
    UserProfileResponse,
    UserProfileUpdate,
)


router = APIRouter()


@router.get(
    "/me/profile",
    response_model=UserProfileResponse,
    summary="Get the current user's musician profile",
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserProfileResponse:

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if profile is None:
        profile = UserProfile(
            user_id=current_user.id,
            experience_level="beginner",
            preferred_learning_level="beginner",
            favorite_ragas=[],
            musical_goals=[],
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


@router.put(
    "/me/profile",
    response_model=UserProfileResponse,
    summary="Create or update the current user's musician profile",
)
def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserProfileResponse:

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if profile is None:
        profile = UserProfile(
            user_id=current_user.id,
            experience_level=profile_data.experience_level,
            preferred_learning_level=(
                profile_data.preferred_learning_level
            ),
            favorite_ragas=profile_data.favorite_ragas,
            musical_goals=profile_data.musical_goals,
        )
        db.add(profile)

    profile.experience_level = profile_data.experience_level
    profile.musical_background = profile_data.musical_background
    profile.primary_instrument = profile_data.primary_instrument
    profile.years_of_experience = profile_data.years_of_experience
    profile.preferred_learning_level = (
        profile_data.preferred_learning_level
    )
    profile.favorite_ragas = profile_data.favorite_ragas
    profile.musical_goals = profile_data.musical_goals

    db.commit()
    db.refresh(profile)

    return profile
