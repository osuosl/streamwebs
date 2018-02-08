#!/usr/bin/env python
import os
import sys
import csv
from datetime import datetime
import requests

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User

from streamwebs.models import GalleryImage  # NOQA
from streamwebs.models import GalleryAlbum  # NOQA
from streamwebs.models import Site  # NOQA
from streamwebs.models import UserProfile


# Change into media directory
os.chdir("../")

if os.path.isdir("./sw_data/"):
    datafile = './sw_data/gallery_csvs/albums.csv'
else:
    datafile = './csvs/gallery_csvs/albums.csv'

# "Title","Gallery Description","Post date","Gallery Id","Picture Description",
#       "Nid","Uid","Filename","Site name","Gallery Image"
with open(datafile, 'r') as csvfile:
    photoreader = csv.reader(csvfile)
    for row in photoreader:
        if 'Title' not in row:  # Skip the header
            album_title = row[0]
            album_description = row[1]
            album_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M')
            album_id = int(row[3])
            image_description = row[4]
            image_id = int(row[5])
            user_id = int(row[6])
            filename = row[7]
            site_title = row[8]
            image_path = row[9]

            # Download image
            dl_file = NamedTemporaryFile(delete=True, dir='.')
            dl_file.write(requests.get(image_path).content)
            dl_file.flush()

            # Get filename
            image_filename = image_path.split('/')[-1]

            # Check for user and their profile
            if user_id:
                album_user = User.objects.filter(
                    id=user_id).first()
                album_user_profile = UserProfile.objects.filter(
                    user=album_user).first()
            else:
                album_user = None
                album_user_profile = None

            # Check for school from profile
            if album_user_profile:
                album_school = album_user_profile.school
            else:
                album_school = None

            # Check for site
            if site_title:
                album_site = Site.objects.filter(
                    site_name=site_title).first()
            else:
                album_site = None

            # Build gallery album
            ga, gac = GalleryAlbum.objects.update_or_create(id=album_id)
            if gac:
                ga.title = album_title
                ga.description = album_description
                ga.date_time = album_date
                ga.site = album_site
                ga.school = album_school
                ga.save()

            # Build gallery image
            gi, gic = GalleryImage.objects.update_or_create(
                id=image_id, title=filename,
                description=image_description,
                site=album_site, user=album_user,
                school=album_school, album=ga
            )
            gi.image.save(image_filename, File(dl_file))

print("Gallery Albums pulled from drupal site and loaded.")
