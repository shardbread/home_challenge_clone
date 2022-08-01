FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME /opt/poetry
ENV PATH $POETRY_HOME/bin:$PATH
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VERSION=1.1.13

COPY app/poetry.lock app/pyproject.toml app/
WORKDIR /app

RUN set -ex \
    && apt-get update && apt-get install -y gcc \
    && pip install --user --upgrade pip \
    && pip install --no-cache-dir \
    "poetry==$POETRY_VERSION" \
    && poetry install

ADD ./app /app
