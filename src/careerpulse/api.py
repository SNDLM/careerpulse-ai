"""CareerPulse REST API."""

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from careerpulse.generative import explain_job
from careerpulse.repository import (
    get_all_jobs,
    get_job_by_id,
    get_job_summary,
    get_madrid_jobs_for_search,
)
from careerpulse.schemas import Job, JobMatch, JobSummary
from careerpulse.semantic import search_jobs

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


@app.get("/jobs/semantic-search", response_model=list[JobMatch])
def semantic_job_search(
    q: Annotated[str, Query(min_length=1, max_length=200)],
    limit: Annotated[int, Query(ge=1, le=20)] = 5,
) -> list[dict[str, object]]:
    """Find Madrid jobs similar to a natural-language query."""
    if not q.strip():
        raise HTTPException(status_code=422, detail="Search query cannot be blank")

    jobs = get_madrid_jobs_for_search()
    return search_jobs(q, jobs, limit=limit)


@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int) -> dict[str, object]:
    """Return one job by its identifier."""
    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

@app.post("/jobs/{job_id}/explanation")
def explain_job_result(
    job_id: int,
    q: Annotated[str, Query(min_length=2, max_length=300)],
) -> dict[str, int | str]:
    """Explain why one job relates to a search."""
    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if not job.get("description"):
        raise HTTPException(
            status_code=422,
            detail="Job has no description",
        )

    if not q.strip():
        raise HTTPException(
            status_code=422,
            detail="Search cannot be empty",
        )

    try:
        explanation = explain_job(q, job)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "job_id": job_id,
        "explanation": explanation,
    }