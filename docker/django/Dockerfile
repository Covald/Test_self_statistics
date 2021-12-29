# pull official base image
FROM python:3.9.6-slim-buster

ARG UID=101
ARG GID=101

# set environment variables
ENV UID=${UID} \
  GID=${GID} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.3 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin" \
  # dockerfile:
  MY_PIP_CONSTRAINT='pip~=21.1.1'

RUN apt-get update && apt-get install -y bash curl libzbar0 \
    && curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
    && poetry --version

WORKDIR /code

COPY ./docker/django/local-entrypoint.sh /local-entrypoint.sh

COPY ./poetry.lock ./pyproject.toml /code/
RUN poetry install

#COPY . /code/
