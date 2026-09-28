"""CareerPulse REST API."""

from fastapi import FastAPI, HTTPException

from careerpulse.repository import get_all_jobs, get_job_by_id
from careerpulse.schemas import Job

app = FastAPI(
    title="CareerPulse AI API",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}


@app.get("/jobs", response_model=list[Job])
def list_jobs(
    technology: str | None = None,
    location: str | None = None,
    remote: bool | None = None,
) -> list[dict[str, object]]:
    """Return job records, optionally filtered."""
    return get_all_jobs(
        technology=technology,
        location=location,
        remote=remote,
    )

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int) -> dict[str, object]:
    """Return one job by its identifier."""
    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job