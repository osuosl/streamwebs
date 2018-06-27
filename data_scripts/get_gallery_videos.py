#!/usr/bin/env python
import os
import sys
import csv
from datetime import datetime
import requests
from streamwebs.models import (GalleryVideo, Site, UserProfile)

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from django.core.files import File # NOQA
from django.core.files.temp import NamedTemporaryFile # NOQA
from django.contrib.auth.models import User # NOQA


# Change into media directory
os.chdir("../")

if os.path.isdir("./sw_data/"):
    datafile = './sw_data/gallery_csvs/videos.csv'
else:
    datafile = './csvs/gallery_csvs/videos.csv'

# "Title", "Description", "Post date", "Nid", "Uid", "Stream/Site name"
#   "Filename", "URL", "Thumbnail Image", "Thumbnail URL"
with open(datafile, 'r') as csvfile:
    video_reader = csv.DictReader(csvfile)
    for row in video_reader:
        title = row['Title']
        description = row['Description']
        date_time = datetime.strptime(row['Post date'], '%Y/%m/%d %H:%M:%S')
        user_id = int(row['Uid'])
        site_name = row['Stream/Site name']
        filename = row['Filename']
        video_path = row['URL']
        thumb_name = row['Thumbnail Image']
        thumb_path = row['Thumbnail URL']

        # Download Video
        if video_path:
            video_file = NamedTemporaryFile(delete=True, dir='.')
            video_file.write(requests.get(video_path).content)
            video_file.flush()
        else:
            video_file = None

        if thumb_path:
            thumb_file = NamedTemporaryFile(delete=True, dir='.')
            thumb_file.write(requests.get(thumb_path).content)
            thumb_file.flush()
        else:
            thumb_file = None

        # Get the filename
        video_filename = video_path.split('/')[-1]
        thumb_filename = thumb_path.split('/')[-1]

        # Get site
        if site_name:
            site = Site.objects.filter(site_name=site_name).first()
        else:
            site = None

        # Get user and user profile
        if user_id:
            user = User.objects.filter(id=user_id).first()
            user_profile = UserProfile.objects.filter(user=user).first()
        else:
            user = None
            user_profile = None

        # Get school
        if user_profile:
            school = user_profile.school
        else:
            school = None

        # Save to database
        gallery_video = GalleryVideo.objects.update_or_create(
            title=title, description=description, site=site, school=school,
            user=user, date_time=date_time
        )
        # Get latest GalleryVideo object
        gv = GalleryVideo.objects.latest('id')

        # Save file if exists
        if video_file:
            gv.video.save(video_filename, File(video_file))
        if thumb_file:
            gv.thumbnail.save(thumb_filename, File(thumb_file))

print("Gallery videos pulled from drupal site and loaded.")
