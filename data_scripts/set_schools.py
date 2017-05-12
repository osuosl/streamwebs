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

from streamwebs.models import Soil_Survey, School  # NOQA

if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/active_schools.csv'
else:
    datafile = '../csvs/active_schools.csv'


with open(datafile, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #if row['School'] != '':
        #print(row['School'])

        # Query Schools for ID
        # school = School.objects.get(nid=row['Nid'])

        if row['Uid'] != '':
            # Check if any soil data sheets were submitted by this user/school
            if Soil_Survey.objects.filter(uid=row['Uid']).exists():
              # Update School field for soil survey
                soil_sheets = []
                soil_survey = Soil_Survey.objects.filter(uid=row['Uid'])

                for each in soil_survey:
                    soil_sheets.append(each.id)

                for each in soil_sheets:
                    #print ('Soil site: ' + str(soil_survey[i]) + '\t' + str(school[0]))
                    soil = Soil_Survey.objects.get(id=each)
                    #print("test: " + str(type(soil_survey[i])))
                    #print("test school: " + str(type(school_key)))
                    soil.school = school.id
                    print (soil)
                    #soil.save()
#        else:
#            print("User: " + row['Uid']  + " not affiliated with school")
#        except streamwebs.models.MultipleObjectsReturned:
#            print(row['School'])  # TODO: Figure out how to deal w/ duplicates

#print "Relations made."
