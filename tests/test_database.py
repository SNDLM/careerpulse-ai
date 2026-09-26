from unittest.mock import Mock

from careerpulse import database


def test_get_connection_uses_environment(monkeypatch) -> None:
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "careerpulse")
    monkeypatch.setenv("DB_USER", "careerpulse_app")
    monkeypatch.setenv("DB_PASSWORD", "test_password")

    expected_connection = Mock()
    mock_connect = Mock(return_value=expected_connection)
    monkeypatch.setattr(database.psycopg, "connect", mock_connect)

    connection = database.get_connection()

    assert connection is expected_connection
    mock_connect.assert_called_once_with(
        host="localhost",
        port="5432",
        dbname="careerpulse",
        user="careerpulse_app",
        password="test_password",
    )