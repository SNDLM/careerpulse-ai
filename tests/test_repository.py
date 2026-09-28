"""Tests for database job queries."""

from unittest.mock import MagicMock, patch

from careerpulse.repository import get_all_jobs, get_job_by_id


def test_get_all_jobs() -> None:
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

    connection_manager = MagicMock()
    connection = MagicMock()
    cursor = MagicMock()

    connection_manager.__enter__.return_value = connection
    connection.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = expected_jobs

    with patch(
        "careerpulse.repository.get_connection",
        return_value=connection_manager,
    ):
        jobs = get_all_jobs()

    cursor.execute.assert_called_once()
    assert jobs == expected_jobs

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

    connection_manager = MagicMock()
    connection = MagicMock()
    cursor = MagicMock()

    connection_manager.__enter__.return_value = connection
    connection.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchone.return_value = expected_job

    with patch(
        "careerpulse.repository.get_connection",
        return_value=connection_manager,
    ):
        job = get_job_by_id(1)

    cursor.execute.assert_called_once()
    assert job == expected_job

def test_get_all_jobs_with_filters() -> None:
    connection_manager = MagicMock()
    connection = MagicMock()
    cursor = MagicMock()

    connection_manager.__enter__.return_value = connection
    connection.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = []

    with patch(
        "careerpulse.repository.get_connection",
        return_value=connection_manager,
    ):
        jobs = get_all_jobs(
            technology="AWS",
            location="Madrid",
            remote=True,
        )

    executed_query, parameters = cursor.execute.call_args.args

    assert "LOWER(technology) = LOWER(%s)" in executed_query
    assert "LOWER(location) = LOWER(%s)" in executed_query
    assert "remote = %s" in executed_query
    assert parameters == ("AWS", "Madrid", True)
    assert jobs == []