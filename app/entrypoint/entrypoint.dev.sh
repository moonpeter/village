#!/bin/sh

if [ "$DATABASE" = "trayd_village" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput
python manage.py migrate

exec "$@"