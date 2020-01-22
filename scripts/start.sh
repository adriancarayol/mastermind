#!/bin/sh

cd /app || exit

echo "Running migrate" && \
python manage.py migrate && \
echo "Starting gunicorn server" && \
gunicorn mastermind.wsgi --bind=0.0.0.0:8000