from careerpulse.main import get_project_name


def test_get_project_name() -> None:
    assert get_project_name() == "CareerPulse AI"