#!/bin/bash

set -euo pipefail

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate
uvicorn marvel_api.asgi:application --host 0.0.0.0 --port 8000
