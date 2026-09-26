CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(200) NOT NULL,
    location VARCHAR(100) NOT NULL,
    technology VARCHAR(100) NOT NULL,
    salary_min INTEGER,
    salary_max INTEGER,
    remote BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_salary_range CHECK (
        salary_min IS NULL
        OR salary_max IS NULL
        OR salary_min <= salary_max
    )
);