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

from streamwebs.models import (
    School, SchoolRelations, Macroinvertebrates, Soil_Survey, 
    RiparianTransect, Water_Quality, Canopy_Cover)

if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/active_schools.csv'
else:
    datafile = '../csvs/active_schools.csv'


with open(datafile, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #if row['School'] != '':
        #print ('??', row['School'])

        # Query Schools for ID
        # school = School.objects.get(nid=row['Nid'])

        if row['Uid'] != '':
            #print (row['Uid'])
            # Check if any soil data sheets were submitted by this user/school
            if Soil_Survey.objects.filter(uid=row['Uid']).exists():
                # Update School field for soil survey
                soil_sheets = []
                soil_survey = Soil_Survey.objects.filter(uid=row['Uid'])

                # Nothing appears to be happening???
                #print ('Got here ' + str(soil_survey))
                #print ('Soil Uid: ' + str(row['Uid']))
                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in soil_survey:
                    soil_sheets.append(each.id)

                # MAKE RELATIONS BETWEEN UID AND SCHOOL
                for each in soil_sheets:
                    #print ('Soil site: ' + str(soil_survey[i]) + '\t' + str(school[0]))
                    soil = Soil_Survey.objects.get(id=each)
                    #print("test: " + str(type(soil_survey[i])))
                    #print("type: " + str(type(relation.school)))
                    soil.school = relation.school
                    #print (soil, 'relation: ' + str(relation.school))
                    soil.save()

            if Macroinvertebrates.objects.filter(uid=row['Uid']).exists():
                # Update School field for soil survey
                macro_sheets = []
                macros = Macroinvertebrates.objects.filter(uid=row['Uid'])

                # Nothing appears to be happening???
                #print ('Got here ' + str(soil_survey))
                #print ('Macro Uid: ' + str(row['Uid']))
                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in macros:
                    macro_sheets.append(each.id)

                # MAKE RELATIONS BETWEEN UID AND SCHOOL
                for each in macro_sheets:
                    #print ('Soil site: ' + str(soil_survey[i]) + '\t' + str(school[0]))
                    macroq = Macroinvertebrates.objects.get(id=each)
                    #print("test: " + str(type(soil_survey[i])))
                    #print("type: " + str(type(relation.school)))
                    macroq.school = relation.school
                    #print (soil, 'relation: ' + str(relation.school))
                    macroq.save()

            if RiparianTransect.objects.filter(uid=row['Uid']).exists():
                # Update School field for soil survey
                rt_sheets = []
                ript = RiparianTransect.objects.filter(uid=row['Uid'])

                # Nothing appears to be happening???
                #print ('Got here ' + str(soil_survey))
                #print ('Uid: ' + str(row['Uid']))
                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in ript:
                    rt_sheets.append(each.id)

                # MAKE RELATIONS BETWEEN UID AND SCHOOL
                for each in rt_sheets:
                    #print ('Soil site: ' + str(soil_survey[i]) + '\t' + str(school[0]))
                    transect = RiparianTransect.objects.get(id=each)
                    #print("test: " + str(type(soil_survey[i])))
                    #print("type: " + str(type(relation.school)))
                    transect.school = relation.school
                    #print (soil, 'relation: ' + str(relation.school))
                    transect.save()

            if Water_Quality.objects.filter(uid=row['Uid']).exists():
                # Update School field for soil survey
                wq_sheets = []
                wq = Water_Quality.objects.filter(uid=row['Uid'])

                # Nothing appears to be happening???
                #print ('Got here ' + str(soil_survey))
                #print ('Uid: ' + str(row['Uid']))
                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in wq:
                    wq_sheets.append(each.id)

                # MAKE RELATIONS BETWEEN UID AND SCHOOL
                for each in wq_sheets:
                    #print ('Soil site: ' + str(soil_survey[i]) + '\t' + str(school[0]))
                    waterq = Water_Quality.objects.get(id=each)
                    #print("test: " + str(type(soil_survey[i])))
                    #print("type: " + str(type(relation.school)))
                    waterq.school = relation.school
                    #print (soil, 'relation: ' + str(relation.school))
                    waterq.save()

            if Canopy_Cover.objects.filter(uid=row['Uid']).exists():
                # Update School field for soil survey
                cc_sheets = []
                cc = Canopy_Cover.objects.filter(uid=row['Uid'])

                # Nothing appears to be happening???
                #print ('Got here ' + str(soil_survey))
                #print ('Uid: ' + str(row['Uid']))
                relation = SchoolRelations.objects.get(uid=row['Uid'])

                for each in cc:
                    cc_sheets.append(each.id)

                # MAKE RELATIONS BETWEEN UID AND SCHOOL
                for each in cc_sheets:
                    #print ('Soil site: ' + str(soil_survey[i]) + '\t' + str(school[0]))
                    canopyc = Canopy_Cover.objects.get(id=each)
                    #print("test: " + str(type(soil_survey[i])))
                    #print("type: " + str(type(relation.school)))
                    canopyc.school = relation.school
                    #print (soil, 'relation: ' + str(relation.school))
                    canopyc.save()

#        else:
#            print("User: " + row['Uid']  + " not affiliated with school")
#        except streamwebs.models.MultipleObjectsReturned:
#            print(row['School'])  # TODO: Figure out how to deal w/ duplicates

#print "Relations made."
