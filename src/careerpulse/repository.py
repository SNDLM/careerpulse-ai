"""Database queries for job records."""

from psycopg.rows import dict_row

from careerpulse.database import get_connection


def get_all_jobs(
    technology: str | None = None,
    location: str | None = None,
    remote: bool | None = None,
) -> list[dict[str, object]]:
    """Return job records, optionally filtered."""
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
    """

    conditions: list[str] = []
    parameters: list[object] = []

    if technology is not None:
        conditions.append("LOWER(technology) = LOWER(%s)")
        parameters.append(technology)

    if location is not None:
        conditions.append("LOWER(location) = LOWER(%s)")
        parameters.append(location)

    if remote is not None:
        conditions.append("remote = %s")
        parameters.append(remote)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY job_id"

    with (
        get_connection() as connection,
        connection.cursor(row_factory=dict_row) as cursor,
    ):
        cursor.execute(query, tuple(parameters))
        return cursor.fetchall()

        
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