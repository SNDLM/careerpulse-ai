"""Client for retrieving job offers from the Adzuna API."""

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def fetch_jobs(
    what: str = "data",
    where: str = "Madrid",
    page: int = 1,
    results_per_page: int = 20,
) -> list[dict[str, Any]]:
    """Retrieve job offers from Adzuna."""

    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    country = os.getenv("ADZUNA_COUNTRY", "es")

    if not app_id or not app_key:
        raise ValueError("Adzuna credentials are missing from the .env file.")

    url = f"{BASE_URL}/{country}/search/{page}"

    params: dict[str, str | int] = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "what": what,
        "where": where,
        "content-type": "application/json",
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Adzuna returned HTTP status {exc.response.status_code}."
        ) from None
    except requests.RequestException:
        raise RuntimeError("Could not connect to Adzuna.") from None
   
    return payload.get("results", [])
        
  