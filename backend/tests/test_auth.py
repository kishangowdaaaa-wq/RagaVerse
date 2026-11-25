from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User


client = TestClient(app)


def create_test_user():
    email = f"auth_{uuid4().hex}@example.com"
    password = "SecurePass123!"

    registration = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "Authentication Tester",
            "email": email,
            "password": password,
        },
    )

    assert registration.status_code == 201

    return email, password


def delete_test_user(email: str):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if user:
            db.delete(user)
            db.commit()
    finally:
        db.close()


def test_successful_login_and_profile_access():
    email, password = create_test_user()

    try:
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": email,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        token_data = login_response.json()

        assert token_data["access_token"]
        assert token_data["token_type"] == "bearer"

        profile_response = client.get(
            "/api/v1/auth/me",
            headers={
                "Authorization": f"Bearer {token_data['access_token']}"
            },
        )

        assert profile_response.status_code == 200

        profile = profile_response.json()

        assert profile["email"] == email
        assert profile["full_name"] == "Authentication Tester"

        assert "hashed_password" not in profile

    finally:
        delete_test_user(email)


def test_login_with_wrong_password():
    email, password = create_test_user()

    try:
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": email,
                "password": "WrongPassword123!",
            },
        )

        assert response.status_code == 401

    finally:
        delete_test_user(email)


def test_profile_without_token():
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_profile_with_invalid_token():
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid.token.value"
        },
    )

    assert response.status_code == 401