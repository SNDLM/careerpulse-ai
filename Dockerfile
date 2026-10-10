FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --no-cache-dir .

COPY dashboard.py ./
COPY tests/fixtures/sample_jobs.csv ./tests/fixtures/sample_jobs.csv

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "careerpulse.api:app", "--host", "0.0.0.0", "--port", "8000"]