#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import School, SchoolRelations # NOQA

if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/active_schools.csv'
else:
    datafile = '../csvs/active_schools.csv'


# If default non-value doesn't exist, create it
unnamed = School.objects.update_or_create(
    name='School unspecified', school_type='Unknown',
    address='Unknown', city='Unknown', province='Unknown',
    zipcode='Unknown'
)

with open(datafile, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Seems like 'Resource Link Charter School' is actually a dup entry
        # B/c one lists a PO Box as an address

        # Butte Falls Charter School seems to have created a new entry, rather
        # than update their address after moving?

        # CASCADE, HOOVER (2), HOWARD, WILSON, EVERGREEN, ROOSEVELT
        # 1781, Jake Slodki, Cascade Middle School (Bend)
        # 163, Jo Albers, Hoover Elementary School (Salem)
        # 1726, Michael Baker, Hoover Elementary School (Corvallis)
        # 1671, Allison Kreider, Howard Elementary School (Eugene)
        # 1101, Sage Randklev, Wilson Elementary School (Medford)
        # 608, Joseph Flaherty, Evergreen Elementary School (Redmond)
        # 83, Barbara Culver, Roosevelt Elementary School (Klamath Falls)

        # ADAMS
        # 1071, Nathan Harris, Adams Elementary School (Corvallis)
        # 1026, Susan Reeves, Adams Elementary School (Corvallis)
        # 188, Joseph Williams, Adams Elementary School (Corvallis)
        # 185, Gerhard Behrens, Adams Elementary School (Corvallis)
        # 182, Laura Lashley, Adams Elementary School (Corvallis)

        school = School.objects.filter(name=row['School'])

        if school.count() > 1:
            for each in school:
                qry = school.first()
                qry.name = str(qry) + ' (' + str(qry.city) + ')'
                qry.save()
        else:
            if row['Uid'] != '':
                uid = row['Uid']
            else:
                uid = None

            # Make relation between uid and school if it exists
            # otherwise, assign a default non-value for school
            if school.exists() and school.count != 0:
                related_school = school.first()
            else:
                related_school = School.objects.get(name='School unspecified')

            relations, created = SchoolRelations.objects.update_or_create(
                uid=uid, school=related_school
            )

print "Duplicates renamed, uid-to-school relations made."
