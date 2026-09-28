"""Tests for the CareerPulse REST API."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from careerpulse.api import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_jobs() -> None:
    expected_jobs = [
        {
            "job_id": 1,
            "title": "Data Engineer",
            "company": "DataWorks",
            "location": "Madrid",
            "technology": "PostgreSQL",
            "salary_min": 32000,
            "salary_max": 42000,
            "remote": False,
        }
    ]

    with patch(
        "careerpulse.api.get_all_jobs",
        return_value=expected_jobs,
    ):
        response = client.get("/jobs")

    assert response.status_code == 200
    assert response.json() == expected_jobs