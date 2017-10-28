#!/bin/bash

trap /home/centos/streamwebs/dockerfiles/cleanup.sh EXIT
bower install --allow-root
yes "yes" | python /home/centos/streamwebs/streamwebs_frontend/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.filter(email='streamwebs@osuosl.org').delete(); User.objects.create_superuser('admin', 'streamwebs@osuosl.org', 'admin')" | python streamwebs_frontend/manage.py shell
python /home/centos/streamwebs/streamwebs_frontend/manage.py runserver 0.0.0.0:8000
