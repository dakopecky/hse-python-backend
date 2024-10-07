.PHONY: docker docker-server docker-test install-deps server test

PORT       ?= 8000
HOST       ?= 0.0.0.0
DOCKER_TAG ?= shop-api:latest

docker:
	docker build \
	--build-arg "PORT=$(PORT)" \
	-t $(DOCKER_TAG) \
	.

docker-server: docker
	docker run --rm -p $(PORT):$(PORT) --name shop-api "$(DOCKER_TAG)"

docker-test: docker
	docker run --rm --name shop-api "$(DOCKER_TAG)" make test

install-deps:
	poetry install

server: install-deps
	poetry run uvicorn shop_api.main:app --reload --host "$(HOST)" --port "$(PORT)"

test:
	poetry run pytest -vv tests/