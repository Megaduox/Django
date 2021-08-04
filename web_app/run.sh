#!/bin/sh

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

gunicorn -b 0.0.0.0:8000 -w 4 super_news.wsgi
