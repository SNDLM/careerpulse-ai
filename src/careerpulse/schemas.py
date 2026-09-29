"""API data models."""

from pydantic import BaseModel


class Job(BaseModel):
    """Public representation of a job record."""

    job_id: int
    title: str
    company: str
    location: str
    technology: str
    salary_min: int | None = None
    salary_max: int | None = None
    remote: bool
    source: str
    source_job_id: str


class JobSummary(BaseModel):
    """Aggregate job-market statistics."""

    total_jobs: int
    average_salary_min: int | None = None
    average_salary_max: int | None = None
    remote_jobs: int