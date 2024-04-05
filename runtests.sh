#!/bin/bash
set -xe
# lint tests
flake8 data_scripts
flake8 streamwebs_frontend/ --exclude streamwebs_frontend/streamwebs/migrations

# run migrations then test
python2 streamwebs_frontend/manage.py makemigrations
python2 streamwebs_frontend/manage.py migrate --noinput
python2 streamwebs_frontend/manage.py test streamwebs_frontend/streamwebs/tests/*
