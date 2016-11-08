#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import RiparianTransect  # NOQA
from streamwebs.models import TransectZone  # NOQA


if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datapath = '../sw_data/'
else:
    datapath = '../csvs/'


transects = datapath + 'rip_transect.csv'
zones = datapath + 'transect_zones.csv'

# Nid, Collected, Site Name, Estimated Slope, Field Notes
with open(transects, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':  # Skip the header
            transect = RiparianTransect()

            if row[3] == '':
                row[3] = None

            # Strip ``Collected date`` so that's in the correct format
            dt = row[1].strip('MonTuesWdhurFiSat(Aly), ')
            transect.date_time = dt

            transect.slope = row[3]
            transect.notes = row[4]
            transect.nid = row[0]

            # Create the foreign key relation between datasheet and site
            site = Site.objects.get(site_name=row[2])
            transect.site_id = site.id

            transect.save()

csvfile.close()
print 'Riparian Transects loaded.'

# 1 - Nid, Conifers, Hardwoods, Shrubs, Comments
# 2 - Conifers, Hardwoods, Shrubs, Comments
# 3 - Conifers, Hardwoods, Shrubs, Comments
# 4 - Conifers, Hardwoods, Shrubs, Comments
# 5 - Conifers, Hardwoods, Shrubs, Comments
with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            zone = TransectZone()

            for i in range(1, 5):
                if row[i] == '':
                    row[i] = None

            zone.zone_num = 1
            zone.conifers = row[1]
            zone.hardwoods = row[2]
            zone.shrubs = row[3]
            zone.comments = row[4]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            zone.transect_id = rip_transect.id

            zone.save()

csvfile.close()
print 'Zone 1 loaded.'

with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            zone = TransectZone()

            for i in range(5, 9):
                if row[i] == '':
                    row[i] = None

            zone.zone_num = 2
            zone.conifers = row[5]
            zone.hardwoods = row[6]
            zone.shrubs = row[7]
            zone.comments = row[8]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            zone.transect_id = rip_transect.id

            zone.save()

csvfile.close()
print 'Zone 2 loaded.'

with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            zone = TransectZone()

            for i in range(9, 13):
                if row[i] == '':
                    row[i] = None

            zone.zone_num = 3
            zone.conifers = row[9]
            zone.hardwoods = row[10]
            zone.shrubs = row[11]
            zone.comments = row[12]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            zone.transect_id = rip_transect.id

            zone.save()

csvfile.close()
print 'Zone 3 loaded.'

with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            zone = TransectZone()

            for i in range(13, 17):
                if row[i] == '':
                    row[i] = None

            zone.zone_num = 4
            zone.conifers = row[13]
            zone.hardwoods = row[14]
            zone.shrubs = row[15]
            zone.comments = row[16]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            zone.transect_id = rip_transect.id

            zone.save()

csvfile.close()
print 'Zone 4 loaded.'

with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            zone = TransectZone()

            for i in range(17, 21):
                if row[i] == '':
                    row[i] = None

            zone.zone_num = 5
            zone.conifers = row[17]
            zone.hardwoods = row[18]
            zone.shrubs = row[19]
            zone.comments = row[20]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            zone.transect_id = rip_transect.id

            zone.save()

csvfile.close()
print 'Zone 5 loaded.'
