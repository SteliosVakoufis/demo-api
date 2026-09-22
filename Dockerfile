FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir ".[dev]"

COPY alembic.ini ./
COPY alembic ./alembic
COPY scripts ./scripts
COPY tools ./tools
COPY tests ./tests

CMD ["sh", "-c", "alembic upgrade head && uvicorn parcel_api.main:app --host 0.0.0.0 --port 8000"]

