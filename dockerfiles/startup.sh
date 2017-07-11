#!/bin/bash

trap /home/centos/streamwebs/dockerfiles/cleanup.sh EXIT
bower install --allow-root
yes "yes" | python /home/centos/streamwebs/streamwebs_frontend/manage.py migrate
python /home/centos/streamwebs/streamwebs_frontend/manage.py runserver 0.0.0.0:8000
