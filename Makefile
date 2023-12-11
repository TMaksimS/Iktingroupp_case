up_test_db:
	docker compose -f docker-compose-local.yaml up -d
migrations: up_test_db
	sleep 2
	alembic upgrade head
down_local:
	docker compose -f docker-compose-local.yaml down --remove-orphans
reboot:
	docker compose -f docker-compose-local.yaml down --remove-orphans
	docker compose -f docker-compose-local.yaml up -d
	sleep 2
	alembic revision --autogenerate -m "Making DB models"
	alembic upgrade head
reboot2:
	docker compose -f docker-compose-local.yaml down --remove-orphans
	docker compose -f docker-compose-local.yaml up -d
	sleep 2
	alembic upgrade head
	sleep 1
	pytest -v
	docker compose -f docker-compose-local.yaml down --remove-orphans
	docker compose -f docker-compose-local.yaml up -d
	sleep 2
	alembic upgrade head
	python3 main.py