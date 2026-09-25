from pathlib import Path

from careerpulse.pipeline import extract_and_transform

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_jobs.csv"


def test_extract_and_transform() -> None:
    jobs = extract_and_transform(FIXTURE_PATH)

    assert len(jobs) == 4
    assert jobs[0]["job_id"] == 1
    assert jobs[0]["technology"] == "PostgreSQL"
    assert jobs[1]["technology"] == "AWS"
    assert jobs[1]["remote"] is True
    assert all(job["location"] == "Madrid" for job in jobs)