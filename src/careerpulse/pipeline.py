"""ETL pipeline orchestration."""

from pathlib import Path

from careerpulse.adzuna import fetch_jobs
from careerpulse.extract import load_jobs_from_csv
from careerpulse.load import (
    save_adzuna_jobs_to_postgres,
    save_jobs_to_csv,
    save_jobs_to_postgres,
)
from careerpulse.transform import transform_adzuna_job, transform_jobs


def extract_and_transform(
    file_path: str | Path,
) -> list[dict[str, str | int | bool]]:
    """Load raw jobs from CSV and return cleaned job records."""
    raw_jobs = load_jobs_from_csv(file_path)
    return transform_jobs(raw_jobs)


def run_etl(
    input_path: str | Path,
    output_path: str | Path,
) -> None:
    """Extract, transform, and save job records."""
    jobs = extract_and_transform(input_path)
    save_jobs_to_csv(jobs, output_path)


def run_etl_to_postgres(input_path: str | Path) -> None:
    """Extract, transform, and save CSV job records to PostgreSQL."""
    jobs = extract_and_transform(input_path)
    save_jobs_to_postgres(jobs)


def run_adzuna_etl(
    what: str = "data",
    where: str = "Madrid",
    page: int = 1,
    results_per_page: int = 20,
) -> int:
    """Extract Adzuna jobs, transform them, and save them to PostgreSQL."""
    raw_jobs = fetch_jobs(
        what=what,
        where=where,
        page=page,
        results_per_page=results_per_page,
    )

    transformed_jobs = [
        transform_adzuna_job(job)
        for job in raw_jobs
    ]

    save_adzuna_jobs_to_postgres(transformed_jobs)

    return len(transformed_jobs)