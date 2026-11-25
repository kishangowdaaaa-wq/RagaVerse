
import pytest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User
from app.api.v1.endpoints import audio, auth, users


client = TestClient(app)


@pytest.fixture
def auth_headers():
    """Create an authenticated test user and provide JWT headers."""

    # Reset endpoint-specific rate limits between test setups.
    users.limiter.reset()
    auth.limiter.reset()
    audio.limiter.reset()

    email = f"audio_{uuid4().hex}@example.com"
    password = "SecurePass123!"

    registration = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "Audio Tester",
            "email": email,
            "password": password,
        },
    )

    assert registration.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    yield {
        "Authorization": f"Bearer {token}"
    }

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if user:
            db.delete(user)
            db.commit()
    finally:
        db.close()


def test_audio_analysis_success(monkeypatch, auth_headers):
    """Verify successful authenticated audio analysis."""

    async def mock_analyze_audio(
        audio_bytes,
        filename,
        tonic_frequency,
    ):
        return {
            "audio": {
                "sample_rate": 22050,
                "duration_seconds": 2.0,
                "channels": 1,
                "waveform": [0.2, 0.5, 0.3],
                "peak_amplitude": 0.5,
            },
            "pitch": {
                "average_frequency": 261.63,
                "frequencies": [261.63],
                "times": [0.0],
                "confidence": [0.95],
                "voiced_frames": 1,
                "total_frames": 1,
                "voiced_ratio": 1.0,
            },
            "swara": {
                "tonic_frequency": tonic_frequency,
                "sequence": [{"swara": "S"}],
                "detected_swaras": ["S"],
            },
            "raga": {
                "candidate_count": 74,
                "candidates": [
                    {"name": "Shankarabharanam"}
                ],
            },
        }

    monkeypatch.setattr(
        audio.audio_service,
        "analyze_audio",
        mock_analyze_audio,
    )

    response = client.post(
        "/api/v1/audio/analyze",
        files={
            "file": (
                "test.wav",
                b"fake audio data",
                "audio/wav",
            )
        },
        data={"tonic_frequency": "261.63"},
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["analysis"]["audio"]["sample_rate"] == 22050
    assert data["analysis"]["swara"]["detected_swaras"] == ["S"]
    assert (
        data["analysis"]["raga"]["candidates"][0]["name"]
        == "Shankarabharanam"
    )


def test_audio_analysis_rejects_empty_file(auth_headers):
    """Verify that empty audio uploads are rejected."""

    response = client.post(
        "/api/v1/audio/analyze",
        files={
            "file": (
                "empty.wav",
                b"",
                "audio/wav",
            )
        },
        data={"tonic_frequency": "261.63"},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_audio_analysis_rejects_invalid_tonic(auth_headers):
    """Verify that a zero tonic frequency is rejected."""

    response = client.post(
        "/api/v1/audio/analyze",
        files={
            "file": (
                "test.wav",
                b"fake audio data",
                "audio/wav",
            )
        },
        data={"tonic_frequency": "0"},
        headers=auth_headers,
    )

    assert response.status_code == 422
    assert "tonic" in response.json()["detail"].lower()


def test_audio_analysis_rejects_unsupported_format(auth_headers):
    """Verify that unsupported audio formats are rejected."""

    response = client.post(
        "/api/v1/audio/analyze",
        files={
            "file": (
                "test.mp3",
                b"fake audio data",
                "audio/mpeg",
            )
        },
        data={"tonic_frequency": "261.63"},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert "unsupported audio format" in (
        response.json()["detail"].lower()
    )


def test_audio_analysis_rejects_missing_file(auth_headers):
    """Verify that an upload without a file is rejected."""

    response = client.post(
        "/api/v1/audio/analyze",
        data={"tonic_frequency": "261.63"},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_audio_analysis_requires_authentication():
    """Verify that audio analysis rejects requests without a JWT."""

    response = client.post(
        "/api/v1/audio/analyze",
        files={
            "file": (
                "test.wav",
                b"fake audio data",
                "audio/wav",
            )
        },
        data={"tonic_frequency": "261.63"},
    )

    assert response.status_code == 401


def test_audio_analysis_rejects_invalid_token():
    """Verify that audio analysis rejects invalid JWTs."""

    response = client.post(
        "/api/v1/audio/analyze",
        files={
            "file": (
                "test.wav",
                b"fake audio data",
                "audio/wav",
            )
        },
        data={"tonic_frequency": "261.63"},
        headers={
            "Authorization": "Bearer invalid.token.value"
        },
    )

    assert response.status_code == 401
