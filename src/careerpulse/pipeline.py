"""ETL pipeline orchestration."""

from pathlib import Path

from careerpulse.extract import load_jobs_from_csv
from careerpulse.load import save_jobs_to_csv
from careerpulse.transform import transform_jobs


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