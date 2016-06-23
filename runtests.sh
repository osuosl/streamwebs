#!/bin/bash

# run migrations then test
python streamwebs_frontend/manage.py makemigrations
python streamwebs_frontend/manage.py migrate
python streamwebs_frontend/manage.py test streamwebs_frontend/streamwebs/tests/models
python streamwebs_frontend/manage.py test streamwebs_frontend/streamwebs/tests/views
