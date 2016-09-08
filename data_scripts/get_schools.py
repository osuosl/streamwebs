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

with open('../csvs/schools_info.csv', 'r') as csvfile:
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

print "Data loaded."
