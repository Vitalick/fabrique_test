#!/usr/bin/env bash

sleep 2;
python manage.py migrate

gunicorn --workers=3  idaproject_test.wsgi:application --bind 0.0.0.0:8000