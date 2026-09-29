"""CareerPulse REST API."""

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from careerpulse.repository import get_all_jobs, get_job_by_id, get_job_summary
from careerpulse.schemas import Job, JobSummary

app = FastAPI(
    title="CareerPulse AI API",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}


@app.get("/stats/summary", response_model=JobSummary)
def job_summary() -> dict[str, object]:
    """Return aggregate job-market statistics."""
    return get_job_summary()


@app.get("/jobs", response_model=list[Job])
def list_jobs(
    technology: str | None = None,
    location: str | None = None,
    remote: bool | None = None,
    source: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[dict[str, object]]:
    """Return filtered and paginated job records."""
    return get_all_jobs(
        technology=technology,
        location=location,
        remote=remote,
        source=source,
        limit=limit,
        offset=offset,
    )


@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int) -> dict[str, object]:
    """Return one job by its identifier."""
    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job