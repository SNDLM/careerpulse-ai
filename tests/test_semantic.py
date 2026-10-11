"""Tests for local semantic job search."""

from unittest.mock import patch

import pytest

from careerpulse.semantic import search_jobs


def test_search_jobs_ranks_by_similarity() -> None:
    jobs = [
        {"job_id": 1, "title": "Frontend Developer", "description": "React UI"},
        {
            "job_id": 2,
            "title": "Data Engineer",
            "description": "<p>Python pipelines</p>",
        },
    ]

    with patch("careerpulse.semantic._get_model") as get_model:
        get_model.return_value.encode.return_value = [
            [1.0, 0.0],  # Query
            [0.0, 1.0],  # Frontend offer
            [0.8, 0.6],  # Data offer
        ]
        results = search_jobs("Trabajo con Python", jobs, limit=1)

    assert len(results) == 1
    assert results[0]["job_id"] == 2
    assert results[0]["similarity"] == 0.8

    texts = get_model.return_value.encode.call_args.args[0]
    assert texts[0] == "query: Trabajo con Python"
    assert texts[1].startswith("passage: ")
    assert "Python pipelines" in texts[2]
    assert "<p>" not in texts[2]


def test_search_jobs_rejects_empty_query() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        search_jobs("   ", [])