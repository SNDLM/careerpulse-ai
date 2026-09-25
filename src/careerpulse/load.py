"""Data loading utilities for processed job records."""

import csv
from pathlib import Path

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