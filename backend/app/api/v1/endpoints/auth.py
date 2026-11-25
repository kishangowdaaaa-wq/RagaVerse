
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.password import verify_password
from app.services.token import create_access_token


router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/login",
    response_model=TokenResponse,
    tags=["Authentication"],
    summary="Login and receive an access token",
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:

    normalized_email = form_data.username.lower()

    user = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    if user is None or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive.",
        )

    access_token = create_access_token(user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,
    tags=["Authentication"],
    summary="Get the currently authenticated user",
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:

    return current_user
