#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/home/centos/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import School  # NOQA

if os.path.isdir("/home/centos/streamwebs/streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/schools_info.csv'
else:
    datafile = '../csvs/schools_info.csv'


with open(datafile, 'r') as csvfile:
    sitereader = csv.DictReader(csvfile)
    for row in sitereader:
        school = School()

        school.name = row['School name']
        school.school_type = row['School type']
        school.address = row['Street']
        school.city = row['City']
        school.province = row['Province'] + ", " + row['Country']
        school.zipcode = row['Postal Code']
        school.save()

print "Schools loaded."
