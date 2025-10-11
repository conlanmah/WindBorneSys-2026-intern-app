#!/bin/sh
python manage.py migrate
exec gunicorn windborne_application.wsgi --bind 0.0.0.0:$PORT
