#!/usr/bin/env python

import os
import sys
import csv
import datetime

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import Water_Quality  # NOQA


if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/wq_csvs/water_quality.csv'
else:
    datafile = '../csvs/wq_csvs/water_quality.csv'


# Stream/Site name, DEQ Data Quality, Collected, School, Any fish present?
# num alive, num dead, Air Temp units, Water Temp units, Lat, Long, Nid

with open(datafile, 'r') as csvfile:
    wqreader = csv.reader(csvfile)
    for row in wqreader:
        if row[0] != 'Stream/Site name':  # Skip header
            for i in range(0, 12):
                if row[i] == '':
                    row[i] = None

            # Strip ``Collected date`` to be YYYY-MM-DD
            t_date = row[2].strip('MonTuesWdhurFiSat(Aly), ')

            # Format datetime object for query
            if len(t_date) > 10:
                date_time =\
                    datetime.datetime.strptime(t_date, '%Y-%m-%d %H:%M').date()

            # Format date object
            collected =\
                datetime.datetime.strptime(t_date[:10], '%Y-%m-%d').date()

            # Date to compare ``collected`` to
            agate1_date =\
                datetime.datetime.strptime('2014-06-09', '%Y-%m-%d').date()

            DEQ_dq_level = row[1]
            school = row[3]   # TODO: Figure out corr. schools

            if row[4] == 'Yes':
                #waterq.fish_present = True
                fish_present = True
            elif row[4] == 'No':
                #waterq.fish_present = False
                fish_present = False
            else:
                #waterq.fish_present = row[4]
                fish_present = row[4]

            live_fish = row[5]
            dead_fish = row[6]

            air_temp_unit = row[7]
            water_temp_unit = row[8]

            latitude = row[9]
            longitude = row[10]

            nid = row[11]

            if row[0] is not None:
                try:
                    site = Site.objects.get(site_name=row[0])
                    site_id = site.id
                except:  # for the one site_name exception...
                    if date_time >= agate1_date:
                        site = Site.objects.get(
                            site_name=row[0], site_slug='agate-beach1')
                        site_id = site.id
                    else:
                        site = Site.objects.get(
                            site_name=row[0], site_slug='agate-beach')
                        site_id = site.id
            else:
                site_id = None

            waterq = Water_Quality.objects.update_or_create(
                date=collected, DEQ_dq_level=DEQ_dq_level, school=school,
                fish_present=fish_present, live_fish=live_fish,
                dead_fish=dead_fish, air_temp_unit=air_temp_unit,
                water_temp_unit=water_temp_unit, latitude=latitude,
                longitude=longitude, nid=nid, site_id=site_id
            )


csvfile.close()

print 'Basic info loaded.'
