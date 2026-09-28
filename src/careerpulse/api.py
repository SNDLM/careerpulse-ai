"""CareerPulse REST API."""

from fastapi import FastAPI

app = FastAPI(
    title="CareerPulse AI API",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}