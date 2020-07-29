#!/usr/bin/env bash

sleep 2;
python manage.py migrate

python manage.py runserver 0.0.0.0:8000