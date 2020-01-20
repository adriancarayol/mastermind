FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.0.2


# deps
RUN pip install "poetry==$POETRY_VERSION"

# Copy poetry files
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false --no-interaction --no-ansi

COPY mastermind /app
