
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_talas_endpoint():
    response = client.get("/api/v1/knowledge/talas")

    assert response.status_code == 200
    assert response.json()["count"] == 5


def test_tala_search():
    response = client.get(
        "/api/v1/knowledge/talas",
        params={"q": "Adi"},
    )

    assert response.status_code == 200
    assert response.json()["count"] >= 1


def test_swaras_endpoint():
    response = client.get("/api/v1/knowledge/swaras")

    assert response.status_code == 200
    assert response.json()["count"] == 7


def test_swara_search():
    response = client.get(
        "/api/v1/knowledge/swaras",
        params={"q": "Shadja"},
    )

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_compositions_endpoint():
    response = client.get(
        "/api/v1/knowledge/compositions"
    )

    assert response.status_code == 200
    assert response.json()["count"] == 6


def test_composition_search_by_raga():
    response = client.get(
        "/api/v1/knowledge/compositions",
        params={"raga": "Kalyani"},
    )

    assert response.status_code == 200
    assert response.json()["count"] >= 1


def test_composition_search_by_composer():
    response = client.get(
        "/api/v1/knowledge/compositions",
        params={"composer": "Tyagaraja"},
    )

    assert response.status_code == 200
    assert response.json()["count"] >= 1
