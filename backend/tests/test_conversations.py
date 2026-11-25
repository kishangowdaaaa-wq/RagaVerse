from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import SessionLocal
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message


client = TestClient(app)


def create_test_user():
    email = f"conversation_{uuid4().hex}@example.com"
    password = "SecurePass123!"

    response = client.post(
        "/api/v1/users/register",
        json={
            "full_name": "Conversation Tester",
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


def delete_test_user(email):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if user:
            db.delete(user)
            db.commit()
    finally:
        db.close()


def test_create_conversation():
    email, headers = create_test_user()

    try:
        response = client.post(
            "/api/v1/conversations/",
            json={"title": "Learning Mayamalavagowla"},
            headers=headers,
        )

        assert response.status_code == 201

        data = response.json()

        assert data["title"] == "Learning Mayamalavagowla"
        assert data["id"] is not None
        assert "created_at" in data
        assert "updated_at" in data

    finally:
        delete_test_user(email)


def test_list_own_conversations():
    email, headers = create_test_user()

    try:
        for title in ["Raga Studies", "Tala Studies"]:
            response = client.post(
                "/api/v1/conversations/",
                json={"title": title},
                headers=headers,
            )
            assert response.status_code == 201

        response = client.get(
            "/api/v1/conversations/",
            headers=headers,
        )

        assert response.status_code == 200

        titles = [item["title"] for item in response.json()]

        assert len(titles) == 2
        assert "Raga Studies" in titles
        assert "Tala Studies" in titles

    finally:
        delete_test_user(email)


def test_get_conversation_with_messages():
    email, headers = create_test_user()

    try:
        create_response = client.post(
            "/api/v1/conversations/",
            json={"title": "Understanding Kalyani"},
            headers=headers,
        )

        assert create_response.status_code == 201

        conversation_id = create_response.json()["id"]

        db = SessionLocal()

        try:
            message = Message(
                conversation_id=conversation_id,
                role="user",
                content="Explain the raga Kalyani.",
            )
            db.add(message)
            db.commit()
        finally:
            db.close()

        response = client.get(
            f"/api/v1/conversations/{conversation_id}",
            headers=headers,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["title"] == "Understanding Kalyani"
        assert len(data["messages"]) == 1
        assert data["messages"][0]["role"] == "user"
        assert data["messages"][0]["content"] == "Explain the raga Kalyani."

    finally:
        delete_test_user(email)


def test_delete_conversation():
    email, headers = create_test_user()

    try:
        create_response = client.post(
            "/api/v1/conversations/",
            json={"title": "Temporary Conversation"},
            headers=headers,
        )

        conversation_id = create_response.json()["id"]

        delete_response = client.delete(
            f"/api/v1/conversations/{conversation_id}",
            headers=headers,
        )

        assert delete_response.status_code == 204

        get_response = client.get(
            f"/api/v1/conversations/{conversation_id}",
            headers=headers,
        )

        assert get_response.status_code == 404

    finally:
        delete_test_user(email)


def test_user_cannot_access_another_users_conversation():
    email_one, headers_one = create_test_user()
    email_two, headers_two = create_test_user()

    try:
        create_response = client.post(
            "/api/v1/conversations/",
            json={"title": "Private Conversation"},
            headers=headers_one,
        )

        conversation_id = create_response.json()["id"]

        get_response = client.get(
            f"/api/v1/conversations/{conversation_id}",
            headers=headers_two,
        )

        assert get_response.status_code == 404

        delete_response = client.delete(
            f"/api/v1/conversations/{conversation_id}",
            headers=headers_two,
        )

        assert delete_response.status_code == 404

        # The original owner must still be able to access it.
        owner_response = client.get(
            f"/api/v1/conversations/{conversation_id}",
            headers=headers_one,
        )

        assert owner_response.status_code == 200

    finally:
        delete_test_user(email_one)
        delete_test_user(email_two)


def test_conversation_access_without_token():
    response = client.get("/api/v1/conversations/")

    assert response.status_code == 401
