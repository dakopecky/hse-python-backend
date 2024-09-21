.PHONY: docker install-deps server test

PORT       ?= 8000
HOST       ?= localhost
DOCKER_TAG ?= ghcr.io/dakopecky/REPOSITORY_NAME

docker:
	docker build \
	-t math-api \
	.

install-deps:
	poetry install

server: install-deps
	poetry run uvicorn main:app --reload --host "$(HOST)" --port "$(PORT)" &

test:
	poetry run pytest tests/

run: server test
