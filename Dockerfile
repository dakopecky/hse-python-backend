FROM python:3.10-slim


RUN apt-get update && apt-get install make
RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock* Makefile ./

RUN make install-deps

COPY . /app

CMD ["make", "run"]
