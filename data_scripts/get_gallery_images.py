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

from streamwebs.models import GalleryImage  # NOQA
from streamwebs.models import Site  # NOQA
from streamwebs.models import UserProfile
from django.contrib.auth.models import User


if os.path.isdir("../sw_data/"):
    datafile = '../sw_data/gallery_csvs/images.csv'
else:
    datafile = '../csvs/gallery_csvs/images.csv'
 

# "Title","Nid","Uid","Site Name","Description","Image" (path)
media_dir = "../media/gallery_images/"
with open(datafile, 'r') as csvfile:
    photoreader = csv.reader(csvfile)
    for row in photoreader:
        if 'Nid' not in row:  # Skip the header

            gallery_image_title = row[0]
            gallery_image_id = row[1]
            gallery_user_id = row[2]
            gallery_image_site = row[3]
            gallery_image_description = row[4]
            image_path = row[5]
            image_file = os.path.basename(image_path)

            try:
                # These files were pulled in via pull-files.sh
                image = open(media_dir + image_file, 'r')

                # Check for site
                if gallery_image_site:
                    gallery_site = Site.objects.filter(
                        site_name=gallery_image_site).first()
                else:
                    gallery_site = None

                # Check for user and their profile
                if gallery_user_id:
                    gallery_user = User.objects.filter(
                        id=gallery_user_id).first()
                    gallery_user_profile = UserProfile.objects.filter(
                        user=gallery_user).first()
                else:
                    gallery_user = None
                    gallery_user_profile = None

                # Check for school from profile
                if gallery_user_profile:
                    gallery_school = gallery_user_profile.school
                else:
                    gallery_school = None

                # Build gallery image
                gi_image = GalleryImage.objects.update_or_create(
                    id=gallery_image_id, title=gallery_image_title,
                    site=gallery_site, user=gallery_user,
                    school=gallery_school,
                    description=gallery_image_description
                )
                gi = GalleryImage.objects.get(id=gallery_image_id)
                gi.image.save(image_file, File(image))
                gi.save()
            except IOError:
                print("Image File not found! " + media_dir + image_file)

print("Gallery Images loaded.")
