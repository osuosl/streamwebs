#!/bin/bash

trap /home/centos/streamwebs/dockerfiles/cleanup.sh EXIT
bower install --allow-root
export PGPASSWORD=$POSTGRES_PASSWORD
echo "Waiting for postgres to start.."
until $(psql -h postgres_host -U $POSTGRES_USER streamwebs \
  -c 'SELECT PostGIS_full_version();' 2> /dev/null | grep -q POSTGIS) ; do
	sleep 1
done
if [ -n "$STREAMWEBS_DROP" ] ; then
  echo "Dropping streamwebs database.."
  psql -h postgres_host -U $POSTGRES_USER streamwebs \
    -c "select pg_terminate_backend(pid) from pg_stat_activity where datname='streamwebs';"
  dropdb -h postgres_host -U $POSTGRES_USER --if-exists streamwebs
  createdb -h postgres_host -U $POSTGRES_USER streamwebs
fi
if [ -n "$STREAMWEBS_TEST" ] ; then
  /home/centos/streamwebs/runtests.sh
else
  yes "yes" | python /home/centos/streamwebs/streamwebs_frontend/manage.py migrate
  echo "from django.contrib.auth.models import User; User.objects.filter(email='streamwebs@osuosl.org').delete(); User.objects.create_superuser('admin', 'streamwebs@osuosl.org', 'admin')" | python streamwebs_frontend/manage.py shell
  if [ -n "$STREAMWEBS_IMPORT_DATA" -a -n "$STREAMWEBS_DROP" ] ; then
    echo "Importing data.."
    cd data_scripts/
    ./get_all.sh
    cd ../
  fi
  python /home/centos/streamwebs/streamwebs_frontend/manage.py runserver 0.0.0.0:8000
fi
