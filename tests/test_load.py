import csv
from pathlib import Path
from unittest.mock import MagicMock, patch

from careerpulse.load import save_jobs_to_csv, save_jobs_to_postgres


def test_save_jobs_to_csv(tmp_path: Path) -> None:
    jobs = [
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
    output_path = tmp_path / "processed_jobs.csv"

    save_jobs_to_csv(jobs, output_path)

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        saved_jobs = list(csv.DictReader(csv_file))

    assert output_path.exists()
    assert len(saved_jobs) == 1
    assert saved_jobs[0]["technology"] == "PostgreSQL"
    assert saved_jobs[0]["salary_min"] == "32000"
    assert saved_jobs[0]["remote"] == "False"

def test_save_jobs_to_postgres() -> None:
    jobs = [
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

    with patch(
        "careerpulse.load.get_connection",
        return_value=connection_manager,
    ):
        save_jobs_to_postgres(jobs)

    cursor.executemany.assert_called_once()
    query, values = cursor.executemany.call_args.args

    assert "INSERT INTO jobs" in query
    assert values == [
        (
            1,
            "Data Engineer",
            "DataWorks",
            "Madrid",
            "PostgreSQL",
            32000,
            42000,
            False,
        )
    ]