.PHONY: up down reset logs migrate seed test lint typecheck verify race readonly-role

up:
	docker compose up --build -d

down:
	docker compose down

reset:
	docker compose down --volumes
	docker compose up --build -d

logs:
	docker compose logs --tail=100 api db

migrate:
	docker compose exec api alembic upgrade head

seed:
	docker compose exec api python scripts/seed.py

test:
	docker compose exec api pytest -q

lint:
	docker compose exec api ruff check .

typecheck:
	docker compose exec api mypy src tools scripts

verify: test lint typecheck

race:
	docker compose exec api python scripts/race_transfer.py

readonly-role:
	docker compose exec -T db psql -U parcels -d parcels < scripts/create_readonly_role.sql

