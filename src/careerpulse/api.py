"""CareerPulse REST API."""

from fastapi import FastAPI

from careerpulse.repository import get_all_jobs

app = FastAPI(
    title="CareerPulse AI API",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}

@app.get("/jobs")
def list_jobs() -> list[dict[str, object]]:
    """Return all job records."""
    return get_all_jobs()