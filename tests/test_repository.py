"""Tests for database job queries."""

from unittest.mock import MagicMock, patch

from careerpulse.repository import get_all_jobs


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