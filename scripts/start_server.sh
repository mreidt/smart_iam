#! /bin/bash

# turn on bash's job control
set -m
python scripts/wait_for_mysql.py
python manage.py migrate --settings="smart_iam.settings.$MODE"

if [ "$MODE" == "development" ];
then
    uwsgi --ini uwsgi.ini --py-autoreload=2 --honour-stdin --workers 1 --threads 2
else
    uwsgi --ini uwsgi.ini --workers 3 --threads 2
fi
