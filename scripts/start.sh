#!/bin/sh

cd /app || exit

echo "Running makemigrations" && \
python manage.py makemigrations && \
echo "Running migrate" && \
python manage.py migrate && \
echo "Starting gunicorn server" && \
gunicorn mastermind.wsgi --bind=0.0.0.0:8000 --reload