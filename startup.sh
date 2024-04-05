#!/bin/bash
trap /usr/src/app/cleanup.sh EXIT
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
  /usr/src/app/runtests.sh
elif [ -n "$STREAMWEBS_IMPORT_DB" ] ; then
  pg_restore -x -h postgres_host -U $POSTGRES_USER -d streamwebs streamwebs.sql
  ./entrypoint.sh
else
  yes "yes" | python2 /usr/src/app/streamwebs_frontend/manage.py migrate
  echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'testing@streamwebs.org', 'admin')" | python2 streamwebs_frontend/manage.py shell
  if [ -n "$STREAMWEBS_IMPORT_DATA" -a -n "$STREAMWEBS_DROP" ] ; then
    echo "Importing data.."
    cd data_scripts/
    ./get_all.sh
    cd ../
  fi
  ./entrypoint.sh
fi
