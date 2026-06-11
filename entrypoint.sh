#!/bin/sh

set -e

echo "Ожидание PostgreSQL..."
while ! nc -z db 5432; do
    sleep 1
done

echo "PostgreSQL готов"

echo "Применяем миграции..."
python manage.py migrate

echo "Собираем статику..."
python manage.py collectstatic --noinput

echo "Запуск Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000