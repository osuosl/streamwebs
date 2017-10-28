#!/usr/bin/env python
import os
import sys
import csv
import re
from datetime import datetime

from django.core.wsgi import get_wsgi_application
# from django.contrib.gis.geos import GEOSGeometry


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import CameraPoint # NOQA
from streamwebs.models import PhotoPoint # NOQA


# Function to convert the (string) coordinates to a float value
def num(x):
    try:
        return float(x)
    except ValueError:
        if x == '':
            return float(0.0)
        else:
            return x


# Function to convert the (string) coordinates to a int value
def num_int(x):
    try:
        return int(num(x))
    except ValueError:
        if x == '':
            return int(0)
        else:
            return x


# Function to convert inches to decimal feet
def inches_to_dec(x):
    try:
        return float(x) / 12
    except ValueError:
        if x == '':
            return float(0.0)
        else:
            return float(x)


if os.path.isdir("../sw_data/"):
    datafile = '../sw_data/photo_points.csv'
else:
    datafile = '../csvs/photo_points.csv'


# Title, Stream/Site name, Collected, Map Datum, Description, Latitude,
# Longitude, Nid
with open(datafile, 'r') as csvfile:
    photoreader = csv.reader(csvfile)
    for row in photoreader:
        if row[0] != 'Title':  # Skip the header

            number = num_int(re.sub('[A-Za-z:]', '', row[0]))
            if number == '':
                number = 1
            photo_point_id = int(row[1])
            camera_point = CameraPoint.objects.get(id=row[2])
            pp_date = datetime.strptime(row[3], "%a, %Y-%m-%d")
            compass_bearing = num_int(row[4])
            distance = num(row[5]) + inches_to_dec(row[6])
            camera_height = num(row[7]) + inches_to_dec(row[8])
            notes = row[9]

            photo_point = PhotoPoint.objects.update_or_create(
                id=photo_point_id, number=number, camera_point=camera_point,
                pp_date=pp_date, compass_bearing=compass_bearing,
                distance=distance, camera_height=camera_height, notes=notes
            )

print "Photo Points loaded."
