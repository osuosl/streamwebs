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

from streamwebs.models import GalleryFile  # NOQA
from streamwebs.models import Site  # NOQA
from streamwebs.models import UserProfile
from django.contrib.auth.models import User


if os.path.isdir("../sw_data/"):
    datafile = '../sw_data/gallery_csvs/files.csv'
else:
    datafile = '../csvs/gallery_csvs/files.csv'
 

# "Title","Nid","Uid","Site Name","Description","File" (path)
media_dir = "../media/gallery_files/"
with open(datafile, 'r') as csvfile:
    photoreader = csv.reader(csvfile)
    for row in photoreader:
        if 'Nid' not in row:  # Skip the header

            gallery_file_title = row[0]
            gallery_file_id = row[1]
            gallery_user_id = row[2]
            gallery_file_site = row[3]
            gallery_file_description = row[4]
            file_path = row[5]
            file_file = os.path.basename(file_path)

            try:
                # These files were pulled in via pull-files.sh
                f = open(media_dir + file_file, 'r')

                # Check for site
                if gallery_file_site:
                    gallery_site = Site.objects.filter(
                        site_name=gallery_file_site).first()
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

                # Build gallery file
                gf_file = GalleryFile.objects.update_or_create(
                    id=gallery_file_id, title=gallery_file_title,
                    site=gallery_site, user=gallery_user,
                    school=gallery_school,
                    description=gallery_file_description
                )
                gf = GalleryFile.objects.get(id=gallery_file_id)
                gf.file.save(file_file, File(f))
                gf.save()
            except IOError:
                print("File not found! " + media_dir + file_file)

print("Gallery Files loaded.")
