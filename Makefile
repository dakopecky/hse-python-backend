.PHONY: docker docker-run install-deps server test

PORT       ?= 8000
HOST       ?= localhost
DOCKER_TAG ?= ghcr.io/dakopecky/hse-python-backend/math-api:latest

docker:
	docker build \
	-t $(DOCKER_TAG) \
	.

docker-run: docker
	docker run --rm --name math-api "$(DOCKER_TAG)"

install-deps:
	poetry install

detached-server: install-deps
	poetry run uvicorn main:app --reload --host "$(HOST)" --port "$(PORT)" &

server: install-deps
	poetry run uvicorn main:app --reload --host "$(HOST)" --port "$(PORT)"

test:
	poetry run pytest tests/

run: detached-server test
