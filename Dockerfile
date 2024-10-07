FROM python:3.10-slim-bookworm

WORKDIR /project

RUN apt update && apt install make

RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY README.md Makefile ./
COPY shop_api ./shop_api
COPY tests ./tests
RUN poetry install

ARG PORT
EXPOSE $PORT

CMD ["make", "server"]
