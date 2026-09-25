"""Data transformation utilities for job-market records."""


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



def normalize_technology(value: str) -> str:
    """Return a consistent display name for a technology."""
    normalized_value = value.strip().lower()
    return TECHNOLOGY_ALIASES.get(normalized_value, normalized_value.title())

def transform_job_record(
    record: dict[str, str],
) -> dict[str, str | int | bool]:
    """Clean and convert a raw job record."""
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
    """Transform a list of raw job records."""
    return [transform_job_record(record) for record in records]