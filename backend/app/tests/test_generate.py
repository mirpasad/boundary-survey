import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_generate_unauthorized():
    r = client.post("/api/surveys/generate", json={"description": "test"})
    assert r.status_code == 401

def test_generate_ok_with_fallback(monkeypatch):
    # bypass DB create since TestClient runs startup
    headers = {"X-API-KEY": "dev-token-123"}
    r = client.post("/api/surveys/generate", headers=headers, json={"description": "coffee shop"})
    assert r.status_code == 201
    data = r.json()
    assert "title" in data and "questions" in data
    assert isinstance(data["questions"], list)
