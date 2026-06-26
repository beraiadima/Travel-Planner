COMPOSE = docker compose

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up

up-d:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

migrations:
	$(COMPOSE) exec travel_planner python manage.py makemigrations

migrate:
	$(COMPOSE) exec travel_planner python manage.py migrate

superuser:
	$(COMPOSE) exec travel_planner python manage.py createsuperuser

shell:
	$(COMPOSE) exec travel_planner python manage.py shell