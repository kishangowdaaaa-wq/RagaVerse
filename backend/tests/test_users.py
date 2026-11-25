
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User
from app.services.password import verify_password


client = TestClient(app)


def test_user_registration():
    email = f"test_{uuid4().hex}@example.com"

    response = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "RagaVerse Tester",
            "email": email,
            "password": "SecurePass123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "RagaVerse Tester"
    assert data["email"] == email
    assert data["is_active"] is True

    # Password and hash must never appear in the API response.
    assert "password" not in data
    assert "hashed_password" not in data

    # Verify that the password was hashed correctly in the database.
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        assert user is not None
        assert user.hashed_password != "SecurePass123!"
        assert verify_password(
            "SecurePass123!",
            user.hashed_password,
        )

    finally:
        if user is not None:
            db.delete(user)
            db.commit()

        db.close()


def test_duplicate_user_registration():
    email = f"duplicate_{uuid4().hex}@example.com"

    payload = {
        "full_name": "Duplicate Tester",
        "email": email,
        "password": "SecurePass123!",
    }

    first_response = client.post(
        "/api/v1/users/register",
        json=payload,
    )

    second_response = client.post(
        "/api/v1/users/register",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if user is not None:
            db.delete(user)
            db.commit()

    finally:
        db.close()
