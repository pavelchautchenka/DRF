#!/bin/sh
chmod +x ./manage.py
python manage.py createsuperuser --noinput;
python manage.py migrate;
python gunicorn -w 2 -b 0.0.0.0:8000 DRF.wsgi:application;