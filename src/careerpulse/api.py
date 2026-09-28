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
def list_jobs() -> list[dict[str, object]]:
    """Return all job records."""
    return get_all_jobs()


@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int) -> dict[str, object]:
    """Return one job by its identifier."""
    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job