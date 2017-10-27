#!/usr/bin/env python
import os
import sys
import csv

from django.core.wsgi import get_wsgi_application
# from django.contrib.gis.geos import GEOSGeometry


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA

if os.path.isdir("../sw_data/"):
    datafile = '../sw_data/sites.csv'
else:
    datafile = '../csvs/sites.csv'


with open(datafile, 'r') as csvfile:
    sitereader = csv.reader(csvfile)
    for row in sitereader:
        if row[0] != '':  # Skip the header
            description = row[7].strip()
            site = Site.objects.filter(site_name=row[0]).update(
                description=description
            )

print "Site Descriptions loaded."
