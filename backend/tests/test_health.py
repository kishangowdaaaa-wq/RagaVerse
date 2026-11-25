
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Welcome to RagaVerse!"
    assert data["status"] == "running"


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["app_name"] == "RagaVerse"
    assert data["version"] == "0.1.0"


def test_health_response_schema():
    response = client.get("/api/v1/health")

    data = response.json()

    assert set(data.keys()) == {
        "status",
        "app_name",
        "version"
    }
