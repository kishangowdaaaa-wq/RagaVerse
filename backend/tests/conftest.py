
import pytest

from app.api.v1.endpoints import auth, users, audio


@pytest.fixture(autouse=True)
def reset_rate_limits():
    """Reset endpoint rate-limit counters before every test."""

    auth.limiter.reset()
    users.limiter.reset()
    audio.limiter.reset()

    yield
