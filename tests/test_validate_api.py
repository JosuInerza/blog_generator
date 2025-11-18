from fastapi.testclient import TestClient
from app.main import app
from app.services.slug_service import clear_store


client = TestClient(app)


def setup_function():
    clear_store()


def test_validate_success():
    resp = client.post("/validate", json={"title": "Hello World"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is True
    assert "slug" in data


def test_validate_title_too_short():
    resp = client.post("/validate", json={"title": "ab"})
    assert resp.status_code == 422
    body = resp.json()
    assert "errors" in body["detail"]
