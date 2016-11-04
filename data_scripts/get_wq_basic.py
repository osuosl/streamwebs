#!/usr/bin/env python

import os
import sys
import csv
import datetime

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/home/centos/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import Water_Quality  # NOQA


if os.path.isdir("/home/centos/streamwebs/streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/wq_csvs/water_quality.csv'
else:
    datafile = '../csvs/wq_csvs/water_quality.csv'


# Stream/Site name, DEQ Data Quality, Collected, School, Any fish present?
# num alive, num dead, Air Temp units, Water Temp units, Lat, Long, Nid

with open(datafile, 'r') as csvfile:
    wqreader = csv.reader(csvfile)
    for row in wqreader:
        if row[0] != 'Stream/Site name':  # Skip header
            waterq = Water_Quality()

            for i in range(0, 12):
                if row[i] == '':
                    row[i] = None

            # Strip ``Collected date`` to be YYYY-MM-DD
            t_date = row[2].strip('MonTuesWdhurFiSat(Aly), ')

            # Formate datetime object for query
            if len(t_date) > 10:
                date_time =\
                    datetime.datetime.strptime(t_date, '%Y-%m-%d %H:%M').date()

            # Format date object
            collected =\
                datetime.datetime.strptime(t_date[:10], '%Y-%m-%d').date()

            waterq.date = collected

            # Date to compare ``collected`` to
            agate1_date =\
                datetime.datetime.strptime('2014-06-09', '%Y-%m-%d').date()

            waterq.DEQ_dq_level = row[1]
            waterq.school = row[3]

            if row[4] == 'Yes':
                waterq.fish_present = True
            elif row[4] == 'No':
                waterq.fish_present = False
            else:
                waterq.fish_present = row[4]

            waterq.live_fish = row[5]
            waterq.dead_fish = row[6]

            waterq.air_temp_unit = row[7]
            waterq.water_temp_unit = row[8]

            waterq.latitude = row[9]
            waterq.longitude = row[10]

            waterq.nid = row[11]

            if row[0] is not None:
                try:
                    site = Site.objects.get(site_name=row[0])
                    waterq.site_id = site.id
                except:  # for the one site_name exception...
                    if date_time >= agate1_date:
                        site = Site.objects.get(
                            site_name=row[0], site_slug='agate-beach1')
                        waterq.site_id = site.id
                    else:
                        site = Site.objects.get(
                            site_name=row[0], site_slug='agate-beach')
                        waterq.site_id = site.id
            else:
                waterq.site_id = None

            waterq.save()

csvfile.close()

print 'Basic info loaded.'
