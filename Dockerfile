FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.0.2


# deps
RUN pip install "poetry==$POETRY_VERSION"

# Copy poetry files
WORKDIR /deps
COPY poetry.lock pyproject.toml /deps/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

# Copy project code
WORKDIR /app
COPY mastermind /app

WORKDIR /script
COPY scripts /script

WORKDIR /app

CMD /wait && /script/start.sh