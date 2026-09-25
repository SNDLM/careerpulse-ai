"""Data extraction utilities for job-market records."""

import csv
from pathlib import Path


def load_jobs_from_csv(file_path: str | Path) -> list[dict[str, str]]:
    """Load job records from a CSV file."""
    path = Path(file_path)

    with path.open(encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))