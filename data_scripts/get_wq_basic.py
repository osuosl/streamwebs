#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/opt/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site
from streamwebs.models import Water_Quality  # NOQA


# Stream/Site name, DEQ Data Quality, Collected, School, Any fish present?
# num alive, num dead, Air Temp units, Water Temp units, Lat, Long, Nid

with open('../csvs/wq_csvs/small/wq.csv', 'r') as csvfile:
    wqreader = csv.reader(csvfile)
    for row in wqreader:
        if row[0] != 'Stream/Site name':  # Skip header
            waterq = Water_Quality()

            for i in range(0, 12):
                if row[i] == '':
                    row[i] = None

            # Strip ``Collected date`` to be YYYY-MM-DD
            collected = row[2].strip('MonTuesWdhurFiSat(Aly), ')
            #print collected

            waterq.date = collected

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

            site = Site.objects.get(site_name=row[0])
            waterq.site_id = site.id

            waterq.save()

csvfile.close()

print 'Basic info loaded.'
