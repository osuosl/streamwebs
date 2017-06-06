#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import (  # NOQA
    SchoolRelations, Macroinvertebrates, Soil_Survey, RiparianTransect,
    Water_Quality, Canopy_Cover)

if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/active_schools.csv'
else:
    datafile = '../csvs/active_schools.csv'


with open(datafile, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Check that uid is valid
        if row['Uid'] != '':
            # Check if any soil data sheets were submitted by this user/school
            if Soil_Survey.objects.filter(uid=row['Uid']).exists():
                # Update School field for soil survey
                soil_sheets = []
                soil_survey = Soil_Survey.objects.filter(uid=row['Uid'])

                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in soil_survey:
                    soil_sheets.append(each.id)

                # MAKE RELATIONS BETWEEN UID AND SCHOOL
                for each in soil_sheets:
                    soil = Soil_Survey.objects.get(id=each)
                    soil.school = relation.school
                    soil.save()

            if Macroinvertebrates.objects.filter(uid=row['Uid']).exists():
                macro_sheets = []
                macros = Macroinvertebrates.objects.filter(uid=row['Uid'])

                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in macros:
                    macro_sheets.append(each.id)

                for each in macro_sheets:
                    macroq = Macroinvertebrates.objects.get(id=each)
                    macroq.school = relation.school
                    macroq.save()

            if RiparianTransect.objects.filter(uid=row['Uid']).exists():
                rt_sheets = []
                ript = RiparianTransect.objects.filter(uid=row['Uid'])

                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in ript:
                    rt_sheets.append(each.id)

                for each in rt_sheets:
                    transect = RiparianTransect.objects.get(id=each)
                    transect.school = relation.school
                    transect.save()

            if Water_Quality.objects.filter(uid=row['Uid']).exists():
                wq_sheets = []
                wq = Water_Quality.objects.filter(uid=row['Uid'])

                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in wq:
                    wq_sheets.append(each.id)

                for each in wq_sheets:
                    waterq = Water_Quality.objects.get(id=each)
                    waterq.school = relation.school
                    waterq.save()

            if Canopy_Cover.objects.filter(uid=row['Uid']).exists():
                cc_sheets = []
                cc = Canopy_Cover.objects.filter(uid=row['Uid'])

                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in cc:
                    cc_sheets.append(each.id)

                for each in cc_sheets:
                    canopyc = Canopy_Cover.objects.get(id=each)
                    canopyc.school = relation.school
                    canopyc.save()

print "Relation between schools and data sheets established."
