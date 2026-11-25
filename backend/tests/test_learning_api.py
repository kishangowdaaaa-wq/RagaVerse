
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_learning_modules():
    response = client.get("/api/v1/learning/")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 7
    assert len(data["results"]) == 7


def test_filter_learning_modules_by_level():
    response = client.get(
        "/api/v1/learning/",
        params={"level": "Beginner"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 7

    for module in data["results"]:
        assert module["level"] == "Beginner"


def test_search_learning_modules():
    response = client.get(
        "/api/v1/learning/",
        params={"q": "Swara"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] >= 1


def test_get_learning_module_details():
    response = client.get(
        "/api/v1/learning/swara_fundamentals"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "swara_fundamentals"
    assert data["title"] == "Swara Fundamentals"
    assert len(data["lessons"]) == 4


def test_learning_module_not_found():
    response = client.get(
        "/api/v1/learning/invalid_module"
    )

    assert response.status_code == 404
