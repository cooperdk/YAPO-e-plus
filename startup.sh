#!/bin/bash

if [ -f "./db.sqlite3" ]; then
  python -u manage.py makemigrations
  python -u manage.py migrate
fi

python -u manage.py runserver 0.0.0.0:8000