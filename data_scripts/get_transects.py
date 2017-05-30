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


#transects = datapath + 'rip_transect.csv'
#zones = datapath + 'transect_zones.csv'
transects = datapath + 'rt_new.csv'
zones = datapath + 'tz_new.csv'


# Nid, Collected, Site Name, Estimated Slope, Field Notes, Uid
with open(transects, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':  # Skip the header
            if row[3] == '' or row[3] == 'n/a':
                row[3] = None

            # Strip ``Collected date`` so that's in the correct format
            date_time = row[1].strip('MonTuesWdhurFiSat(Aly), ')

            slope = row[3]
            notes = row[4]
            nid = row[0]
            uid = row[5]

            # Create the foreign key relation between datasheet and site
            site = Site.objects.get(site_name=row[2])
            site_id = site.id

            # For some reason, the last datasheet keeps being duplicated?
            # So check to make sure it doesn't exist before creating obj
            if not RiparianTransect.objects.filter(nid=nid).exists():
                transect = RiparianTransect.objects.create(
                    date_time=date_time, slope=slope, notes=notes, nid=nid,
                    site_id=site_id, uid=uid
                )

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
            # Set entry == None if value is not listed in csv
            for i in range(1, 4):
                if row[i] == '':
                    row[i] = None

            zone_num = 1
            conifers = row[1]
            hardwoods = row[2]
            shrubs = row[3]
            comments = row[4]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            transect_id = rip_transect.id

            zone = TransectZone.objects.update_or_create(
                zone_num=zone_num, conifers=conifers, hardwoods=hardwoods,
                shrubs=shrubs, comments=comments, transect_id=transect_id
            )

csvfile.close()
print 'Zone 1 loaded.'

with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            for i in range(5, 8):
                if row[i] == '':
                    row[i] = None

            zone_num = 2
            conifers = row[5]
            hardwoods = row[6]
            shrubs = row[7]
            comments = row[8]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            transect_id = rip_transect.id

            zone = TransectZone.objects.update_or_create(
                zone_num=zone_num, conifers=conifers, hardwoods=hardwoods,
                shrubs=shrubs, comments=comments, transect_id=transect_id
            )

csvfile.close()
print 'Zone 2 loaded.'

with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            for i in range(9, 12):
                if row[i] == '':
                    row[i] = None

            zone_num = 3
            conifers = row[9]
            hardwoods = row[10]
            shrubs = row[11]
            comments = row[12]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            transect_id = rip_transect.id

            zone = TransectZone.objects.update_or_create(
                zone_num=zone_num, conifers=conifers, hardwoods=hardwoods,
                shrubs=shrubs, comments=comments, transect_id=transect_id
            )

csvfile.close()
print 'Zone 3 loaded.'

with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            for i in range(13, 16):
                if row[i] == '':
                    row[i] = None

            zone_num = 4
            conifers = row[13]
            hardwoods = row[14]
            shrubs = row[15]
            comments = row[16]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            transect_id = rip_transect.id

            zone = TransectZone.objects.update_or_create(
                zone_num=zone_num, conifers=conifers, hardwoods=hardwoods,
                shrubs=shrubs, comments=comments, transect_id=transect_id
            )

csvfile.close()
print 'Zone 4 loaded.'

with open(zones, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nid':
            for i in range(17, 20):
                if row[i] == '':
                    row[i] = None

            zone_num = 5
            conifers = row[17]
            hardwoods = row[18]
            shrubs = row[19]
            comments = row[20]

            # Create the foreign key relation between datasheet and site
            rip_transect = RiparianTransect.objects.get(nid=row[0])
            transect_id = rip_transect.id

            zone = TransectZone.objects.update_or_create(
                zone_num=zone_num, conifers=conifers, hardwoods=hardwoods,
                shrubs=shrubs, comments=comments, transect_id=transect_id
            )

csvfile.close()
print 'Zone 5 loaded.'
