from careerpulse.transform import (
    normalize_technology,
    transform_adzuna_job,
    transform_job_record,
    transform_jobs,
)


def test_normalize_known_aliases() -> None:
    assert normalize_technology("POSTGRES") == "PostgreSQL"
    assert normalize_technology("powerbi") == "Power BI"
    assert normalize_technology("js") == "JavaScript"
    assert normalize_technology("k8s") == "Kubernetes"


def test_remove_spaces_and_ignore_capitalization() -> None:
    assert normalize_technology("  aws  ") == "AWS"


def test_normalize_unknown_technology() -> None:
    assert normalize_technology("docker") == "Docker"


def test_transform_job_record() -> None:
        raw_job = {
            "job_id": "2",
            "title": "Cloud Engineer",
            "company": "CloudTech",
            "location": "Madrid",
            "technology": "  aws  ",
            "salary_min": "45000",
            "salary_max": "60000",
            "remote": "true",
        }

        transformed_job = transform_job_record(raw_job)

        assert transformed_job["job_id"] == 2
        assert transformed_job["technology"] == "AWS"
        assert transformed_job["salary_min"] == 45000
        assert transformed_job["remote"] is True

def test_transform_jobs() -> None:
    raw_jobs = [
        {
            "job_id": "1",
            "title": "Data Engineer",
            "company": "DataWorks",
            "location": "Madrid",
            "technology": "POSTGRES",
            "salary_min": "32000",
            "salary_max": "42000",
            "remote": "false",
        }
    ]

    transformed_jobs = transform_jobs(raw_jobs)

    assert len(transformed_jobs) == 1
    assert transformed_jobs[0]["technology"] == "PostgreSQL"
    assert transformed_jobs[0]["salary_min"] == 32000
    assert transformed_jobs[0]["remote"] is False

def test_transform_adzuna_job() -> None:
    raw_job = {
        "id": "5875138129",
        "title": "Python Data Engineer",
        "description": "Remote role building data pipelines.",
        "company": {"display_name": "Nexthink"},
        "location": {"display_name": "Madrid"},
        "salary_min": 42000.5,
        "salary_max": None,
    }

    transformed_job = transform_adzuna_job(raw_job)

    assert transformed_job == {
        "title": "Python Data Engineer",
        "company": "Nexthink",
        "location": "Madrid",
        "technology": "Python",
        "salary_min": 42000,
        "salary_max": None,
        "remote": True,
        "source": "adzuna",
        "source_job_id": "5875138129",
    }