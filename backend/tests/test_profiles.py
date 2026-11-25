
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User


client = TestClient(app)


def create_test_user():
    email = f"profile_{uuid4().hex}@example.com"
    password = "SecurePass123!"

    response = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "Profile Tester",
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return email, {
        "Authorization": f"Bearer {token}"
    }


def delete_test_user(email: str):
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == email
        ).first()

        if user:
            db.delete(user)
            db.commit()

    finally:
        db.close()


def test_get_default_musician_profile():
    email, headers = create_test_user()

    try:
        response = client.get(
            "/api/v1/users/me/profile",
            headers=headers,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["experience_level"] == "beginner"
        assert data["preferred_learning_level"] == "beginner"
        assert data["favorite_ragas"] == []
        assert data["musical_goals"] == []

    finally:
        delete_test_user(email)


def test_update_musician_profile():
    email, headers = create_test_user()

    payload = {
        "experience_level": "intermediate",
        "musical_background": "Learning Carnatic music.",
        "primary_instrument": "Vocal",
        "years_of_experience": 3,
        "preferred_learning_level": "intermediate",
        "favorite_ragas": [
            "Kalyani",
            "Mohanam",
        ],
        "musical_goals": [
            "Improve swara identification",
            "Learn compositions",
        ],
    }

    try:
        response = client.put(
            "/api/v1/users/me/profile",
            json=payload,
            headers=headers,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["experience_level"] == "intermediate"
        assert data["primary_instrument"] == "Vocal"
        assert data["years_of_experience"] == 3
        assert data["favorite_ragas"] == [
            "Kalyani",
            "Mohanam",
        ]

    finally:
        delete_test_user(email)


def test_profile_preferences_persist():
    email, headers = create_test_user()

    payload = {
        "experience_level": "advanced",
        "musical_background": "Advanced Carnatic music training.",
        "primary_instrument": "Violin",
        "years_of_experience": 8,
        "preferred_learning_level": "advanced",
        "favorite_ragas": ["Bhairavi"],
        "musical_goals": ["Master raga alapana"],
    }

    try:
        update_response = client.put(
            "/api/v1/users/me/profile",
            json=payload,
            headers=headers,
        )

        assert update_response.status_code == 200

        get_response = client.get(
            "/api/v1/users/me/profile",
            headers=headers,
        )

        assert get_response.status_code == 200

        data = get_response.json()

        assert data["experience_level"] == "advanced"
        assert data["primary_instrument"] == "Violin"
        assert data["favorite_ragas"] == ["Bhairavi"]
        assert data["musical_goals"] == [
            "Master raga alapana"
        ]

    finally:
        delete_test_user(email)


def test_profile_requires_authentication():
    get_response = client.get(
        "/api/v1/users/me/profile"
    )

    put_response = client.put(
        "/api/v1/users/me/profile",
        json={},
    )

    assert get_response.status_code == 401
    assert put_response.status_code == 401


def test_users_only_access_their_own_profiles():
    email_a, headers_a = create_test_user()
    email_b, headers_b = create_test_user()

    try:
        client.put(
            "/api/v1/users/me/profile",
            json={
                "experience_level": "advanced",
                "primary_instrument": "Veena",
                "favorite_ragas": ["Kalyani"],
                "musical_goals": ["Advanced practice"],
            },
            headers=headers_a,
        )

        response_b = client.get(
            "/api/v1/users/me/profile",
            headers=headers_b,
        )

        assert response_b.status_code == 200

        data_b = response_b.json()

        assert data_b["experience_level"] == "beginner"
        assert data_b["primary_instrument"] is None
        assert data_b["favorite_ragas"] == []

    finally:
        delete_test_user(email_a)
        delete_test_user(email_b)
