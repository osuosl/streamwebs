#!/usr/bin/env python
import os
import sys
import csv
from datetime import datetime

from django.core.wsgi import get_wsgi_application
# from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import CameraPoint # NOQA


# Function to convert the (string) coordinates to a float value
def num(x):
    try:
        return float(x)
    except ValueError:
        return x


if os.path.isdir("../sw_data/"):
    datafile = '../sw_data/camera_points.csv'
else:
    datafile = '../csvs/camera_points.csv'


# Title, Post date, Updated date, Marker, Coordinates, Lat, Long
with open(datafile, 'r') as csvfile:
    sitereader = csv.reader(csvfile)
    for row in sitereader:
        if row[0] != 'Title':  # Skip the header

            letter = row[0]
            site = Site.objects.get(site_name=row[1])
            # Replace any "All day" entrys with 12:00
            dt = row[2].replace('(All day)', '12:00')
            cp_date = datetime.strptime(dt, "%a, %Y-%m-%d %H:%M")
            map_datum = row[3]
            description = row[4]
            # Adjust input data to proper former
            if map_datum == 'WGS 84':
                map_datum = 'WGS84'
            if map_datum == 'NAD 27':
                map_datum = 'NAD27'
            if map_datum == 'NAD 32':
                map_datum = 'NAD32'
            if map_datum == 'NAD 83':
                map_datum = 'NAD83'
            if map_datum == 'NAD 1983':
                map_datum = 'NAD83'
            if map_datum == 'WGS 85':
                map_datum = 'WGS85'
            # Convert latitude and longitude to floats
            lat = num(row[5])
            lng = num(row[6])

            if (lat != '' and lng != ''):  # Skip if there are no coordinates
                pnt = Point(lng, lat)
            location = pnt
            id = row[7]

            camera_point = CameraPoint.objects.update_or_create(
                id=id, site=site, cp_date=cp_date, location=location,
                map_datum=map_datum, description=description
            )

print "Camera Points loaded."
