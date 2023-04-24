#!/bin/bash

set -euo pipefail

poetry run python manage.py collectstatic --noinput
uvicorn marvel_api.asgi:application --host 0.0.0.0 --port 8000
