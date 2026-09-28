"""Tests for the CareerPulse REST API."""

from fastapi.testclient import TestClient

from careerpulse.api import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}