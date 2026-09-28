"""Database queries for job records."""

from psycopg.rows import dict_row

from careerpulse.database import get_connection


def get_all_jobs() -> list[dict[str, object]]:
    """Return all job records from PostgreSQL."""
    query = """
        SELECT
            job_id,
            title,
            company,
            location,
            technology,
            salary_min,
            salary_max,
            remote
        FROM jobs
        ORDER BY job_id
    """

    with (
        get_connection() as connection,
        connection.cursor(row_factory=dict_row) as cursor,
    ):
        cursor.execute(query)
        return cursor.fetchall()

def get_job_by_id(job_id: int) -> dict[str, object] | None:
    """Return one job by its identifier."""
    query = """
        SELECT
            job_id,
            title,
            company,
            location,
            technology,
            salary_min,
            salary_max,
            remote
        FROM jobs
        WHERE job_id = %s
    """

    with (
        get_connection() as connection,
        connection.cursor(row_factory=dict_row) as cursor,
    ):
        cursor.execute(query, (job_id,))
        return cursor.fetchone()