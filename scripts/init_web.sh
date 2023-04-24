#!/bin/bash

set -euo pipefail

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate
# poetry run python manage.py runserver 0.0.0.0:8000
uvicorn marvel_api.asgi:application --host 0.0.0.0 --port 8000
