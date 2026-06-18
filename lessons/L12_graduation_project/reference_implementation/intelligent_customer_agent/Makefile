.PHONY: init build-kb test eval run docker-build docker-up docker-down smoke

PORT ?= 8011

init:
	bash init.sh

build-kb:
	python scripts/build_kb.py

test:
	pytest -q

eval:
	python evals/run_eval.py

run:
	PORT=$(PORT) bash scripts/run_api.sh

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

smoke:
	curl -f http://127.0.0.1:$(PORT)/health
