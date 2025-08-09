#!/bin/sh

echo "Collecting static files"
uv run manage.py collectstatic --noinput

echo "Apply database migrations"
uv run manage.py migrate

echo "Starting Gunicorn"
uv run gunicorn restaurant_reservation_system.wsgi:application --bind 0.0.0.0:8000
