BEGIN;

CREATE SEQUENCE jobs_job_id_seq;

ALTER SEQUENCE jobs_job_id_seq OWNED BY jobs.job_id;

SELECT setval(
    'jobs_job_id_seq',
    COALESCE((SELECT MAX(job_id) FROM jobs), 0) + 1,
    false
);

ALTER TABLE jobs
    ALTER COLUMN job_id SET DEFAULT nextval('jobs_job_id_seq'),
    ADD COLUMN source VARCHAR(50) NOT NULL DEFAULT 'csv',
    ADD COLUMN source_job_id VARCHAR(255);

UPDATE jobs
SET source_job_id = job_id::TEXT;

ALTER TABLE jobs
    ALTER COLUMN source_job_id SET NOT NULL,
    ADD CONSTRAINT jobs_source_job_id_unique
        UNIQUE (source, source_job_id);

GRANT USAGE, SELECT ON SEQUENCE jobs_job_id_seq TO careerpulse_app;

COMMIT;