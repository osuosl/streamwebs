#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/opt/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import School  # NOQA


# Function to convert the (string) coordinates to a float value
def num(x):
    try:
        return float(x)
    except ValueError:
        return x

# Title, Post date, Updated date, Marker, Coordinates, Lat, Long
with open('../csvs/schools_info.csv', 'r') as csvfile:
    sitereader = csv.DictReader(csvfile)
    for row in sitereader:
        school = School()
        print row['School name']
        print row['School type']
        print row['Street']
        print row['City']
        print row['Province']
        print row['Postal Code']
        print row['Country']
        print ""

        """
        school.name = row['School name']
        school.school_type = ['School type']
        school.address =
        school.city =
        school.zipcode =
        school.save()
        """
        """

        # Reassign colored marker to its corresponding site type
        if row[3] == 'small blue':
            site.site_type = 'Student Stewardship Project'
        if row[3] == 'small orange':
            site.site_type = 'Salmon Watch'

        site.site_name = row[0]
        site.created = row[1]
        site.modified = row[2]

        # Converting latitude and longitude to floats
        lat = num(row[5])
        lng = num(row[6])
        if (lat != '' and lng != ''):  # Skip if there are no coordinates
            pnt = Point(lat, lng)
        site.location = pnt

        # Save site data to django db
        site.save()
        """

print "Data loaded."
