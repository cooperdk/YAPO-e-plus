#!/bin/bash

# if the database does not exist: do makemigrations/migrate, because they initialize the db
python -u manage.py makemigrations
python -u manage.py migrate

# TODO if the database DOES exist: check version of the database and if migrations are needed.
# as this is no feature yet, just run makemigrations / migrate on every startup

python -u manage.py runserver 0.0.0.0:8000
