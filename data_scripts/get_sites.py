#!/usr/bin/env python

import os
import sys
import platform
import csv

from django.core.wsgi import get_wsgi_application
# from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/home/centos/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA


# Function to convert the (string) coordinates to a float value
def num(x):
    try:
        return float(x)
    except ValueError:
        return x


if os.path.isdir("/home/centos/streamwebs/streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/ll_site_data.csv'
else:
    datafile = '../csvs/ll_site_data.csv'


# Title, Post date, Updated date, Marker, Coordinates, Lat, Long
with open(datafile, 'r') as csvfile:
    sitereader = csv.reader(csvfile)
    for row in sitereader:
        if row[0] != '':  # Skip the header
            site = Site()

            site.site_name = row[0]
            site.created = row[1]
            site.modified = row[2]

            # Converting latitude and longitude to floats
            lat = num(row[5])
            lng = num(row[6])
            if (lat != '' and lng != ''):  # Skip if there are no coordinates
                pnt = Point(lng, lat)
            site.location = pnt

            # Save site data to django db
            site.save()

print "Sites loaded."
