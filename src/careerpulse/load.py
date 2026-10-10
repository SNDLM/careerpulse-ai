"""Data loading utilities for processed job records."""

import csv
from pathlib import Path

from careerpulse.database import get_connection

JOB_FIELDS = [
    "job_id",
    "title",
    "company",
    "location",
    "technology",
    "salary_min",
    "salary_max",
    "remote",
]

ADZUNA_JOB_FIELDS = [
    "title",
    "company",
    "location",
    "technology",
    "salary_min",
    "salary_max",
    "remote",
    "source",
    "source_job_id",
]


def save_jobs_to_csv(
    jobs: list[dict[str, str | int | bool]],
    file_path: str | Path,
) -> None:
    """Save cleaned job records to a CSV file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=JOB_FIELDS)
        writer.writeheader()
        writer.writerows(jobs)


def save_jobs_to_postgres(
    jobs: list[dict[str, str | int | bool]],
) -> None:
    """Save cleaned CSV job records to PostgreSQL."""
    if not jobs:
        return

    query = """
        INSERT INTO jobs (
            title,
            company,
            location,
            technology,
            salary_min,
            salary_max,
            remote,
            source,
            source_job_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (source, source_job_id) DO UPDATE SET
            title = EXCLUDED.title,
            company = EXCLUDED.company,
            location = EXCLUDED.location,
            technology = EXCLUDED.technology,
            salary_min = EXCLUDED.salary_min,
            salary_max = EXCLUDED.salary_max,
            remote = EXCLUDED.remote
    """

    values = [
        (
            *(job[field] for field in JOB_FIELDS[1:]),
            "csv",
            str(job["job_id"]),
        )
        for job in jobs
    ]

    with (
        get_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.executemany(query, values)


def save_adzuna_jobs_to_postgres(
    jobs: list[dict[str, str | int | bool | None]],
) -> None:
    """Save transformed Adzuna job records to PostgreSQL."""
    if not jobs:
        return

    query = """
        INSERT INTO jobs (
            title,
            company,
            location,
            technology,
            salary_min,
            salary_max,
            remote,
            source,
            source_job_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (source, source_job_id) DO UPDATE SET
            title = EXCLUDED.title,
            company = EXCLUDED.company,
            location = EXCLUDED.location,
            technology = EXCLUDED.technology,
            salary_min = EXCLUDED.salary_min,
            salary_max = EXCLUDED.salary_max,
            remote = EXCLUDED.remote
    """

    values = [
        tuple(job[field] for field in ADZUNA_JOB_FIELDS)
        for job in jobs
    ]

    with (
        get_connection() as connection,
        connection.cursor() as cursor,
    ):
        cursor.executemany(query, values)