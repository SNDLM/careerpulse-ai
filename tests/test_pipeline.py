import csv
from pathlib import Path

from careerpulse.pipeline import extract_and_transform, run_etl

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_jobs.csv"


def test_extract_and_transform() -> None:
    jobs = extract_and_transform(FIXTURE_PATH)

    assert len(jobs) == 4
    assert jobs[0]["job_id"] == 1
    assert jobs[0]["technology"] == "PostgreSQL"
    assert jobs[1]["technology"] == "AWS"
    assert jobs[1]["remote"] is True
    assert all(job["location"] == "Madrid" for job in jobs)

def test_run_etl(tmp_path: Path) -> None:
    output_path = tmp_path / "processed_jobs.csv"

    run_etl(FIXTURE_PATH, output_path)

    with output_path.open(encoding="utf-8", newline="") as csv_file:
        processed_jobs = list(csv.DictReader(csv_file))

    assert output_path.exists()
    assert len(processed_jobs) == 4
    assert processed_jobs[0]["technology"] == "PostgreSQL"
    assert processed_jobs[1]["technology"] == "AWS"
    assert processed_jobs[3]["location"] == "Madrid"