from careerpulse.transform import normalize_technology


def test_normalize_known_aliases() -> None:
    assert normalize_technology("POSTGRES") == "PostgreSQL"
    assert normalize_technology("powerbi") == "Power BI"
    assert normalize_technology("js") == "JavaScript"
    assert normalize_technology("k8s") == "Kubernetes"


def test_remove_spaces_and_ignore_capitalization() -> None:
    assert normalize_technology("  aws  ") == "AWS"


def test_normalize_unknown_technology() -> None:
    assert normalize_technology("docker") == "Docker"