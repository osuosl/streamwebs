#!/usr/bin/env python
import os
import sys
import csv
import requests

from django.core.wsgi import get_wsgi_application
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import GalleryFile  # NOQA
from streamwebs.models import Site  # NOQA
from streamwebs.models import UserProfile

# Change into media directory
os.chdir("../")

if os.path.isdir("./sw_data/"):
    datafile = './sw_data/gallery_csvs/files.csv'
else:
    datafile = './csvs/gallery_csvs/files.csv'

# "Title","Nid","Uid","Site Name","Description","File" (path)
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

            # Download image
            dl_file = NamedTemporaryFile(delete=True, dir='.')
            dl_file.write(requests.get(file_path).content)
            dl_file.flush()

            # Get filename
            file_filename = file_path.split('/')[-1]

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
            gf.gallery_file.save(file_filename, File(dl_file))


print("Gallery Files pulled from drupal site and loaded.")
