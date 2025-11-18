from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Blog Generator API" in r.json()["message"]


def test_create_and_get_item():
    r = client.post("/api/v1/items/", json={"title": "Test", "content": "Contenido"})
    assert r.status_code == 201
    item = r.json()
    assert item["id"] == 1
    r2 = client.get("/api/v1/items/1")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Test"
