#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import School  # NOQA

if os.path.isdir("../streamwebs_frontend/sw_data/"):
    # Update this at some point
    datafile = '../sw_data/schools_info.csv'
else:
    datafile = '../csvs/schools_info.csv'


with open(datafile, 'r') as csvfile:
    sitereader = csv.DictReader(csvfile)
    for row in sitereader:
        # nid = row['Nid']
        name = row['School name']
        school_type = row['School type']
        address = row['Street']
        city = row['City']
        province = row['Province'] + ", " + row['Country']
        zipcode = row['Postal Code']

        school = School.objects.update_or_create(
            name=name, school_type=school_type, address=address, city=city,
            province=province, zipcode=zipcode #, nid=nid
        )

print "Schools loaded."
