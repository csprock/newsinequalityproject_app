#!/bin/bash
sleep 5
echo "Running initialization script..."

if [[ $INIT_DB -eq 1 ]]
then
    echo "Initializing database..."
    flask db init
fi

flask db migrate
flask db upgrade

gunicorn main:app -w 2 -b 0.0.0.0:8000 --timeout 1200 --reload
