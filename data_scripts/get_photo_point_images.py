#!/usr/bin/env python
import os
import sys
import csv
from datetime import datetime

from django.core.wsgi import get_wsgi_application
from django.core.files import File
# from django.contrib.gis.geos import GEOSGeometry


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import PhotoPoint # NOQA
from streamwebs.models import PhotoPointImage # NOQA


if os.path.isdir("../sw_data/"):
    datafile = '../sw_data/photo_point_images.csv'
else:
    datafile = '../csvs/photo_point_images.csv'


# Nid, Photo Point ID, Date, Image
with open(datafile, 'r') as csvfile:
    photoreader = csv.reader(csvfile)
    for row in photoreader:
        if row[0] != 'Nid':  # Skip the header

            pp_image_id = row[0]
            photo_point = PhotoPoint.objects.get(id=row[1])
            date = datetime.strptime(row[2], "%a, %Y-%m-%d")
            image_file = os.path.basename(row[3])
            # These files were pulled in via pull-files.sh
            image = open("../media/pp_photos/" + image_file, 'r')

            try:
                pp_image = PhotoPointImage.objects.update_or_create(
                    id=pp_image_id, photo_point=photo_point, date=date
                )
                ppi = PhotoPointImage.objects.get(id=pp_image_id)
                ppi.image.save(image_file, File(image))
                ppi.save
            except IOError:
                print("Photo Point Image not found! " + image_file)

print "Photo Point Images loaded."
