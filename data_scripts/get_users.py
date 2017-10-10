#!/usr/bin/env python

import os
import sys
import csv
import string
import random

from django.core.wsgi import get_wsgi_application
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from django.contrib.auth.models import User  # NOQA
from streamwebs.models import UserProfile, School  # NOQA

# users file columns:
# "Uid","Name","E-mail","Active","Created date","Last login","Last access",
# "Roles","# of Submissions","School","First name","Last name","Date of birth"

if os.path.isdir("../sw_data/"):
    users_list = '../sw_data/users.csv'
else:
    users_list = '../csvs/users.csv'

with open(users_list, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # skip if no last login
        if not row['Last login'] == '':
            last_login = datetime.strptime(row['Last login'], '%Y-%m-%d %H:%M')

            # skip if last login was more than 3 years ago
            if last_login < datetime.now() - timedelta(days=1095):
                continue

            if row["Uid"]:
                uid = row["Uid"]
            if row["Name"]:
                username = row["Name"]
            if row["First name"]:
                firstname = row["First name"]
            else:
                firstname = ""
            if row["Last name"]:
                lastname = row["Last name"]
            else:
                lastname = ""
            if row["E-mail"]:
                email = row["E-mail"]
            if row["Created date"]:
                created = datetime.strptime(row["Created date"],
                                            '%Y-%m-%d %H:%M')
            if row["Active"]:
                active = row["Active"]
            if row["Roles"]:
                roles = row["Roles"]
            else:
                roles = "Student"

            if row["School"]:
                users_school = row["School"]
            else:
                users_school = ""

            if row["Date of birth"]:
                dob = row["Date of birth"]
                dob = datetime.strptime(row["Date of birth"], '%m/%d/%Y')
            else:
                dob = datetime.strptime('01/01/1970', '%m/%d/%Y')

            password = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(12))

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, password=password,
                    first_name=firstname, last_name=lastname, email=email,
                    date_joined=created
                )
                if School.objects.filter(name=users_school).exists():
                    school = School.objects.filter(name=users_school).first()
                else:
                    school = School.objects.get(name='Unknown School')
                userprofile = UserProfile.objects.update_or_create(
                    user=user, school=school, birthdate=dob)

print "Users loaded."
