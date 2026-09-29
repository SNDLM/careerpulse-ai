"""Data transformation utilities for job-market records."""

import re
from typing import Any

TECHNOLOGY_ALIASES = {
    "amazon web services": "AWS",
    "aws": "AWS",
    "gcp": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "node": "Node.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "python": "Python",
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "sql": "SQL",
    "typescript": "TypeScript",
    "ts": "TypeScript",
}

REMOTE_KEYWORDS = (
    "remote",
    "remoto",
    "teletrabajo",
    "hybrid",
    "híbrido",
    "hibrido",
)


def normalize_technology(value: str) -> str:
    """Return a consistent display name for a technology."""
    normalized_value = value.strip().lower()
    return TECHNOLOGY_ALIASES.get(normalized_value, normalized_value.title())


def detect_technology(text: str) -> str:
    """Detect a known technology inside a job title or description."""
    normalized_text = text.lower()

    aliases = sorted(TECHNOLOGY_ALIASES, key=len, reverse=True)

    for alias in aliases:
        pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"

        if re.search(pattern, normalized_text):
            return TECHNOLOGY_ALIASES[alias]

    return "Unknown"


def transform_job_record(
    record: dict[str, str],
) -> dict[str, str | int | bool]:
    """Clean and convert a raw CSV job record."""
    return {
        "job_id": int(record["job_id"]),
        "title": record["title"].strip(),
        "company": record["company"].strip(),
        "location": record["location"].strip(),
        "technology": normalize_technology(record["technology"]),
        "salary_min": int(record["salary_min"]),
        "salary_max": int(record["salary_max"]),
        "remote": record["remote"].strip().lower() == "true",
    }


def transform_jobs(
    records: list[dict[str, str]],
) -> list[dict[str, str | int | bool]]:
    """Transform a list of raw CSV job records."""
    return [transform_job_record(record) for record in records]


def _get_display_name(value: Any) -> str:
    """Extract display_name from an Adzuna nested object."""
    if isinstance(value, dict):
        display_name = str(value.get("display_name") or "").strip()

        if display_name:
            return display_name

    return "Unknown"


def _optional_integer(value: Any) -> int | None:
    """Convert an optional numeric value to an integer."""
    if value is None:
        return None

    return int(float(value))


def transform_adzuna_job(
    record: dict[str, Any],
) -> dict[str, str | int | bool | None]:
    """Convert an Adzuna result into a CareerPulse job record."""
    title = str(record.get("title") or "").strip()
    description = str(record.get("description") or "").strip()
    company = _get_display_name(record.get("company"))
    location = _get_display_name(record.get("location"))

    searchable_text = f"{title} {description} {location}".lower()

    return {
        "title": title,
        "company": company,
        "location": location,
        "technology": detect_technology(f"{title} {description}"),
        "salary_min": _optional_integer(record.get("salary_min")),
        "salary_max": _optional_integer(record.get("salary_max")),
        "remote": any(
            keyword in searchable_text for keyword in REMOTE_KEYWORDS
        ),
        "source": "adzuna",
        "source_job_id": str(record["id"]),
    }