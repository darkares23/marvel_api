
ifdef NO_DETACH
	detach=
else
	detach=--detach
endif

pytest-default-args=--numprocesses auto

export DOCKER_BUILDKIT=1

nginx/local.crt nginx/local.key:
	@scripts/create_certs.sh

create_certs: nginx/local.crt

build: # Build docker images
	docker-compose build

up: # Ups all the services
	docker-compose up $(detach) web nginx redis celery

stop:
	docker-compose down

superuser: # creates a super user
	docker-compose run --rm web python manage.py createsuperuser

makemigrations: ## Generate migration files for current models changes
	docker-compose run --rm web python manage.py makemigrations

migrate: ## Apply all database migrations
	docker-compose run --rm web python manage.py migrate

test: ## Run tests using pytest
	docker-compose run --rm web poetry run pytest

autoformat: ## Auto-format the entire codebase with black (pass files="..." to run on specific files or paths)
	docker-compose run --rm --no-deps test black $(or $(files),.)

poetry_add:
	docker-compose run --rm web poetry add --lock $(PACKAGES)
