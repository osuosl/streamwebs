#!/bin/sh
echo "Setting permissions to media..."
chown -R nobody:nobody /usr/src/app/media
echo "Running db migrations..."
yes "yes" | python2 /usr/src/app/streamwebs_frontend/manage.py migrate
echo "Starting gunicorn.."
exec gunicorn \
  -u nobody \
  -g nobody \
  --access-logfile '-' \
  --error-logfile '-' \
  --log-file "-" \
  --access-logformat '%({x-forwarded-for}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
  --forwarded-allow-ips="140.211.9.50,140.211.9.52,140.211.9.53" \
  -w 4 \
  -b 0.0.0.0:8000 \
  --chdir streamwebs_frontend \
  'streamwebs_frontend.wsgi:application'
