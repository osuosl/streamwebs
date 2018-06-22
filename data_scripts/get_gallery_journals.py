#!/usr/bin/env python
import os
import sys
import csv
from datetime import datetime

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from django.contrib.auth.models import User
from streamwebs.models import (GalleryJournal, UserProfile, Site) # NOQA

# Change into media directory
os.chdir("../")

if os.path.isdir("./sw_data/"):
    datafile = './sw_data/gallery_csvs/field_journals.csv'
else:
    datafile = './csvs/gallery_csvs/field_journals.csv'

# "Title", "Journal Entry Field", "Post Date", "Nid", "Uid", "Stream/Site name"
with open(datafile, 'r') as csvfile:
    journal_reader = csv.DictReader(csvfile)
    for row in journal_reader:
        # Map data to variables
        title = row['Title']
        journal_entry = row['Journal Entry Field']
        date_time = datetime.strptime(row['Post date'], '%Y-%m-%d %H:%M')
        user_id = int(row['Uid'])
        site_name = row['Stream/Site name']

        # Get user
        if user_id:
            user = User.objects.filter(id=user_id).first()
            user_profile = UserProfile.objects.filter(user=user).first()
        else:
            user = None
            user_profile=None

        # Get school from user profile
        if user_profile:
            school = user_profile.school
        else:
            school = None

        # Get site
        if site_name:
            site = Site.objects.filter(site_name=site_name).first()
        else:
            site = None

        # Add/Update table entry in database
        gallery_journal = GalleryJournal.objects.update_or_create(
            title=title, entry_field=journal_entry, date_time=date_time,
            user=user, school=school, site=site
        )

print("Gallery Journals pulled from drupal site and loaded.")
