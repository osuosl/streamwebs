#!/usr/bin/env python
import os
import sys
import csv

from django.core.wsgi import get_wsgi_application
from django.core.files import File
# from django.contrib.gis.geos import GEOSGeometry


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA

if os.path.isdir("../sw_data/"):
    datafile = '../sw_data/site_images.csv'
else:
    datafile = '../csvs/site_images.csv'


# Site Name, Image
with open(datafile, 'r') as csvfile:
    sitereader = csv.reader(csvfile)
    for row in sitereader:
        if row[0] != 'Site Name':  # Skip the header

            image_file = os.path.basename(row[1])
            # These files were pulled in via pull-files.sh
            image = open("../media/site_photos/" + image_file, 'r')

            site = Site.objects.get(site_name=row[0])
            site.image.save(image_file, File(image))
            site.save

print "Site Images loaded."
