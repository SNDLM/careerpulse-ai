"""ETL pipeline orchestration."""

from pathlib import Path

from careerpulse.extract import load_jobs_from_csv
from careerpulse.transform import transform_jobs


def extract_and_transform(
    file_path: str | Path,
) -> list[dict[str, str | int | bool]]:
    """Load raw jobs from CSV and return cleaned job records."""
    raw_jobs = load_jobs_from_csv(file_path)
    return transform_jobs(raw_jobs)