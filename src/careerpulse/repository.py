"""Database queries for job records."""

from psycopg.rows import dict_row

from careerpulse.database import get_connection


def get_all_jobs(
    technology: str | None = None,
    location: str | None = None,
    remote: bool | None = None,
    source: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[dict[str, object]]:
    """Return filtered and paginated job records."""
    query = """
        SELECT
            job_id,
            title,
            company,
            location,
            technology,
            salary_min,
            salary_max,
            remote,
            source,
            source_job_id
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

    if source is not None:
        conditions.append("LOWER(source) = LOWER(%s)")
        parameters.append(source)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY job_id LIMIT %s OFFSET %s"
    parameters.extend([limit, offset])

    with (
        get_connection() as connection,
        connection.cursor(row_factory=dict_row) as cursor,
    ):
        cursor.execute(query, tuple(parameters))
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
            remote,
            source,
            source_job_id
        FROM jobs
        WHERE job_id = %s
    """

    with (
        get_connection() as connection,
        connection.cursor(row_factory=dict_row) as cursor,
    ):
        cursor.execute(query, (job_id,))
        return cursor.fetchone()


def get_job_summary() -> dict[str, object]:
    """Return aggregate statistics for all jobs."""
    query = """
        SELECT
            COUNT(*) AS total_jobs,
            ROUND(AVG(salary_min))::INTEGER AS average_salary_min,
            ROUND(AVG(salary_max))::INTEGER AS average_salary_max,
            COUNT(*) FILTER (WHERE remote = TRUE) AS remote_jobs
        FROM jobs
    """

    with (
        get_connection() as connection,
        connection.cursor(row_factory=dict_row) as cursor,
    ):
        cursor.execute(query)
        summary = cursor.fetchone()

    if summary is None:
        return {
            "total_jobs": 0,
            "average_salary_min": None,
            "average_salary_max": None,
            "remote_jobs": 0,
        }

    return summary