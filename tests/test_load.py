import csv
from pathlib import Path

from careerpulse.load import save_jobs_to_csv


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