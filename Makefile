# S-001: up, down, logs, smoke targets
# Imports: docker compose, curl
# Exports: make targets

PORT ?= 8080

.PHONY: up down logs smoke

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

smoke:
	curl -fsS localhost:$(PORT)/api/health
	@echo

openapi:
	docker compose run --rm --no-deps -v $(CURDIR)/apps/web:/out api python /app/scripts/export_openapi.py /out/openapi.json
	cd apps/web && npx openapi-typescript openapi.json -o src/api/schema.d.ts