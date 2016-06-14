#!/bin/bash

trap /opt/streamwebs/dockerfiles/cleanup.sh EXIT
bower install --allow-root
python /opt/streamwebs/streamwebs_frontend/manage.py runserver 0.0.0.0:8000
