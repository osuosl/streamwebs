#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/opt/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from django.contrib.auth.models import User  # NOQA
from streamwebs.models import UserProfile, School  # NOQA


with open('../csvs/users1.csv', 'r') as csvfile:
    sitereader = csv.DictReader(csvfile)
    for row in sitereader:
        # print row

        if row["Uid"]:
            uid = row["Uid"]
        if row["Name"]:
            username = row["Name"]
        if row["E-mail"]:
            email = row["E-mail"]
        if row["Created date"]:
            created = row["Created date"]
        if row["Active"]:
            active = row["Active"]
        if row["Roles"]:
            roles = row["Roles"]
        else:
            roles = "Student"

        # row["# of Submissions"]
        with open('../csvs/users2.csv', 'r') as csvfile2:
            sitereader2 = csv.DictReader(csvfile2)
            for row2 in sitereader2:
                if row["Uid"] == row2["Uid"]:
                    first = row2["First name"]
                    last = row2["Last name"]

                    if row2["Date of birth"]:
                        dob = row2["Date of birth"]
                        dob = datetime.strptime(row2["Date of birth"],
                                                '%B %d, %Y')
                    else:
                        dob = "1970-1-1"

                    if row2["School"]:
                        users_school = row2["School"]
                    else:
                        school = ""

        user = User.objects.create_user(username=username,
                                        password="TOOHARDTOGETTOO!@#$",
                                        first_name=first,
                                        last_name=last,
                                        email=email,
                                        date_joined=created
                                        )
        school = School.objects.filter(name=users_school)
        userprofile = UserProfile.objects.create(user=user,
                                                 school=school,
                                                 birthdate=dob)


print "Data loaded."
