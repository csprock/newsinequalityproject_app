#!/bin/bash

sleep 5

if [[ $INIT_DB -eq 1 ]]
then
    flask db init
fi

flask db migrate
flask db upgrade

if [[ $INIT_DB -eq 1 ]]
then
    python seed_database.py
fi

gunicorn main:app -w 2 -b 0.0.0.0:8000 --timeout 1200 --reload
