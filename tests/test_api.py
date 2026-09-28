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

def test_get_job_by_id() -> None:
    expected_job = {
        "job_id": 1,
        "title": "Data Engineer",
        "company": "DataWorks",
        "location": "Madrid",
        "technology": "PostgreSQL",
        "salary_min": 32000,
        "salary_max": 42000,
        "remote": False,
    }

    with patch(
        "careerpulse.api.get_job_by_id",
        return_value=expected_job,
    ):
        response = client.get("/jobs/1")

    assert response.status_code == 200
    assert response.json() == expected_job


def test_get_job_by_id_not_found() -> None:
    with patch(
        "careerpulse.api.get_job_by_id",
        return_value=None,
    ):
        response = client.get("/jobs/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}