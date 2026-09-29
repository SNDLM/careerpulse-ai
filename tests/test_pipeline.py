import csv
from pathlib import Path
from unittest.mock import patch

from careerpulse.pipeline import (
    extract_and_transform,
    run_adzuna_etl,
    run_etl,
    run_etl_to_postgres,
)

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


def test_run_etl_to_postgres() -> None:
    with patch(
        "careerpulse.pipeline.save_jobs_to_postgres",
    ) as mock_save:
        run_etl_to_postgres(FIXTURE_PATH)

    mock_save.assert_called_once()

    jobs = mock_save.call_args.args[0]

    assert len(jobs) == 4
    assert all(job["location"] == "Madrid" for job in jobs)
    assert jobs[0]["technology"] == "PostgreSQL"


def test_run_adzuna_etl() -> None:
    raw_jobs = [
        {
            "id": "5875138129",
            "title": "Python Data Engineer",
            "description": "Remote position using Python.",
            "company": {"display_name": "Nexthink"},
            "location": {"display_name": "Madrid"},
            "salary_min": 42000,
            "salary_max": None,
        }
    ]

    with (
        patch(
            "careerpulse.pipeline.fetch_jobs",
            return_value=raw_jobs,
        ) as mock_fetch,
        patch(
            "careerpulse.pipeline.save_adzuna_jobs_to_postgres",
        ) as mock_save,
    ):
        processed_count = run_adzuna_etl(
            what="data",
            where="Madrid",
            results_per_page=5,
        )

    mock_fetch.assert_called_once_with(
        what="data",
        where="Madrid",
        page=1,
        results_per_page=5,
    )
    mock_save.assert_called_once()

    saved_jobs = mock_save.call_args.args[0]

    assert processed_count == 1
    assert saved_jobs[0]["title"] == "Python Data Engineer"
    assert saved_jobs[0]["technology"] == "Python"
    assert saved_jobs[0]["source"] == "adzuna"
    assert saved_jobs[0]["source_job_id"] == "5875138129"