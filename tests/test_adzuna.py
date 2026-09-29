"""Tests for the Adzuna API client."""

import pytest

from careerpulse.adzuna import fetch_jobs


class FakeResponse:
    """Simulated successful response from Adzuna."""

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict[str, list[dict[str, str]]]:
        return {"results": [{"title": "Data Engineer"}]}


def test_fetch_jobs_returns_results(monkeypatch) -> None:
    monkeypatch.setenv("ADZUNA_APP_ID", "test-id")
    monkeypatch.setenv("ADZUNA_APP_KEY", "test-key")
    monkeypatch.setenv("ADZUNA_COUNTRY", "es")

    def fake_get(
        url: str,
        params: dict[str, str | int],
        timeout: int,
    ) -> FakeResponse:
        assert "/es/search/1" in url
        assert params["where"] == "Madrid"
        assert timeout == 15
        return FakeResponse()

    monkeypatch.setattr("careerpulse.adzuna.requests.get", fake_get)

    jobs = fetch_jobs()

    assert jobs == [{"title": "Data Engineer"}]


def test_fetch_jobs_requires_credentials(monkeypatch) -> None:
    monkeypatch.delenv("ADZUNA_APP_ID", raising=False)
    monkeypatch.delenv("ADZUNA_APP_KEY", raising=False)

    with pytest.raises(ValueError, match="credentials"):
        fetch_jobs()