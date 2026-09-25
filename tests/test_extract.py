from pathlib import Path

from careerpulse.extract import load_jobs_from_csv

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_jobs.csv"


def test_load_jobs_from_csv() -> None:
    jobs = load_jobs_from_csv(FIXTURE_PATH)

    assert len(jobs) == 4
    assert jobs[0]["title"] == "Data Engineer"
    assert jobs[0]["company"] == "DataWorks"
    assert jobs[3]["location"] == "Madrid"