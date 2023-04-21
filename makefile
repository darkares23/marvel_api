
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

collect_statics_and_migratios:
	@scripts/init_web.sh

build: # Build docker images
	docker-compose build

up: # Ups all the services
	docker-compose up $(detach) web nginx redis rqworker

stop:
	docker-compose down

superuser: # Ups all the services
	docker-compose run --rm web python manage.py createsuperuser

makemigrations: ## Generate migration files for current models changes
	docker-compose run --rm web python manage.py makemigrations

migrate: ## Apply all database migrations
	docker-compose run --rm web python manage.py migrate

poetry_add:
	docker-compose run --rm web poetry add --lock $(PACKAGES)
