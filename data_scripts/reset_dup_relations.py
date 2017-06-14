#!/usr/bin/env python

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import School, SchoolRelations # NOQA


# Manually assigning uid-to-school relations for renamed duplicates...
adams_uids = [1071, 1026, 188, 185, 182]
other_uids = [1781, 163, 1726, 1671, 1101, 608, 83]
assoc_schools = ['Cascade Middle School (Bend)',
                 'Hoover Elementary School (Salem)',
                 'Hoover Elementary School (Corvallis)',
                 'Howard Elementary School (Eugene)',
                 'Wilson Elementary School (Medford)',
                 'Evergreen Elementary School (Redmond)',
                 'Roosevelt Elementary School (Klamath Falls)']

for i in range(len(other_uids)):
    uid = other_uids[i]
    related_school = School.objects.get(name=assoc_schools[i])
    relation = SchoolRelations.objects.get(uid=uid)
    relation.school = related_school
    relation.save()

# Make one query since the following uids are associated w/ the same school
related_school = School.objects.get(name='Adams Elementary School (Corvallis)')
for each in adams_uids:
    uid = each
    relation = SchoolRelations.objects.get(uid=uid)
    relation.school = related_school
    relation.save()

print "Uid-to-school relations reset."
