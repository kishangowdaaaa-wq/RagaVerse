
import pytest
from pydantic import ValidationError

from app.core.config import Settings


def valid_settings():
    return {
        "db_password": "test_database_password",
        "secret_key": "a" * 40,
        "environment": "testing",
    }


def test_valid_security_configuration():
    settings = Settings(**valid_settings())

    assert settings.environment == "testing"
    assert len(settings.secret_key.get_secret_value()) >= 32


def test_rejects_weak_secret_key():
    values = valid_settings()
    values["secret_key"] = "weak-secret"

    with pytest.raises(ValidationError):
        Settings(**values)


def test_rejects_unsupported_environment():
    values = valid_settings()
    values["environment"] = "staging"

    with pytest.raises(ValidationError):
        Settings(**values)


def test_rejects_unsupported_jwt_algorithm():
    values = valid_settings()
    values["algorithm"] = "none"

    with pytest.raises(ValidationError):
        Settings(**values)


def test_rejects_invalid_token_expiration():
    values = valid_settings()
    values["access_token_expire_minutes"] = 0

    with pytest.raises(ValidationError):
        Settings(**values)


def test_rejects_invalid_ollama_url():
    values = valid_settings()
    values["ollama_base_url"] = "ftp://localhost:11434"

    with pytest.raises(ValidationError):
        Settings(**values)
