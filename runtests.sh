#!/bin/bash
set -x
# lint tests
flake8 data_scripts
flake8 streamwebs_frontend/ --exclude streamwebs_frontend/streamwebs/migrations

# run migrations then test
python streamwebs_frontend/manage.py makemigrations
python streamwebs_frontend/manage.py migrate --noinput
python streamwebs_frontend/manage.py test streamwebs_frontend/streamwebs/tests/*
