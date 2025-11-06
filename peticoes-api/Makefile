    .PHONY: up down logs rebuild db-init fmt

    up:
		docker compose up -d --build

    down:
		docker compose down

    logs:
		docker compose logs -f api

    rebuild:
		docker compose build --no-cache api && docker compose up -d api

    db-init:
		docker compose exec api python scripts/apply_migrations.py

    fmt:
		autopep8 -r --in-place app || true
