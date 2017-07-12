#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application
# from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA


# Function to convert the (string) coordinates to a float value
def num(x):
    try:
        return float(x)
    except ValueError:
        return x


if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/sites.csv'
else:
    datafile = '../csvs/sites.csv'


# Title, Post date, Updated date, Marker, Coordinates, Lat, Long
with open(datafile, 'r') as csvfile:
    sitereader = csv.reader(csvfile)
    for row in sitereader:
        if row[0] != '':  # Skip the header
            site_name = row[0]
            created = row[1]
            modified = row[2]

            # Convert latitude and longitude to floats
            lat = num(row[5])
            lng = num(row[6])

            if (lat != '' and lng != ''):  # Skip if there are no coordinates
                pnt = Point(lng, lat)
            location = pnt

            site = Site.objects.update_or_create(
                site_name=site_name, created=created, modified=modified,
                location=location
            )

print "Sites loaded."
