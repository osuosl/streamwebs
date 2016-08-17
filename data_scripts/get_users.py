#!/usr/bin/env python

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/opt/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from streamwebs.models import Water_Quality 

import csv

with open('../csvs/active_data_prod.csv', 'r') as csvfile:
    sitereader = csv.reader(csvfile)
    for row in sitereader:
        #if row[0] != 'Marker':  # skip the header 
        #    site = Site()
        #    if row[0] == 'small blue':
        #        site.site_type = 'Student Stewardship Project'
        #    if row[0] == 'small orange':
        #        site.site_type = 'Salmon Watch'
        #    site.site_name = row[1]
        #    site.created = row[2]
        #    site.save()
        print row
