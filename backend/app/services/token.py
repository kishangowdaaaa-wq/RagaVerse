
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import get_settings

settings = get_settings()


def create_access_token(user_id: int) -> str:
    """
    Generate a signed JWT access token for a user.
    """

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    token = jwt.encode(
        payload,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )

    return token


def decode_access_token(token: str) -> dict:
    """
    Verify and decode a JWT access token.
    """

    return jwt.decode(
        token,
        settings.secret_key.get_secret_value(),
        algorithms=[settings.algorithm],
    )
