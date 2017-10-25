#!/usr/bin/env python
import os
import sys
import csv
from datetime import datetime

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
# Set proj path to be relative to data_scripts directory
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import RipAquaticSurvey # NOQA


if os.path.isdir("../sw_data/"):
    datafile = '../sw_data/rip_aquatic_survey.csv'
else:
    datafile = '../csvs/rip_aquatic_survey.csv'


# nid, site, riffle_count, pool_count, collected, silt, sand, gravel, cobble,
# boulders, bedrock, small_debris, medium_debris, large_debris, comments,
# coniferous_trees, deciduous_trees, shrubs, small_plants, ferns, grasses,
# species, significance, wildlife_type, wildlife_comments
with open(datafile, 'r') as csvfile:
    ripareader = csv.reader(csvfile)
    for row in ripareader:
        if row[0] != 'nid':  # Skip the header

            id = row[0]
            site = Site.objects.get(site_name=row[1])
            stream_length = row[2]
            if row[3] == '':
                riffle_count = 0
            else:
                riffle_count = row[3]
            if row[4] == '':
                pool_count = 0
            else:
                pool_count = row[4]
            # Replace any "All day" entrys with 12:00
            dt = row[5].replace('(All day)', '12:00')
            ripa_date = datetime.strptime(dt, "%a, %Y-%m-%d %H:%M")
            silt = row[6]
            sand = row[7]
            gravel = row[8]
            cobble = row[9]
            boulders = row[10]
            bedrock = row[11]
            small_debris = row[12]
            medium_debris = row[13]
            large_debris = row[14]
            comments = row[15]
            coniferous_trees = row[16]
            deciduous_trees = row[17]
            shrubs = row[18]
            small_plants = row[19]
            ferns = row[20]
            grasses = row[21]

            rip_aquatic_survey = RipAquaticSurvey.objects.update_or_create(
                id=id, site=site, riffle_count=riffle_count,
                pool_count=pool_count, date_time=ripa_date, silt=silt,
                sand=sand, gravel=gravel, cobble=cobble, boulders=boulders,
                bedrock=bedrock, small_debris=small_debris,
                medium_debris=medium_debris, large_debris=large_debris,
                comments=comments, coniferous_trees=coniferous_trees,
                deciduous_trees=deciduous_trees, shrubs=shrubs,
                small_plants=small_plants, ferns=ferns, grasses=grasses
            )

print "Riparian Aquatic Surveys loaded."
