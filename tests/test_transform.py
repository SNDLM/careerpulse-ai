from careerpulse.transform import normalize_technology, transform_job_record


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