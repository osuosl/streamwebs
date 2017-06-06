#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Soil_Survey, Site  # NOQA
from streamwebs.util.ft_to_m import feet_to_meters  # NOQA


if os.path.isdir("../streamwebs_frontend/sw_data"):
    datafile = '../sw_data/soil_survey.csv'
else:
    datafile = '../csvs/soil_survey.csv'


# Collected, Stream/Site name, Landscape Position, Cover Type, Land Use,
# Distance From Stream, Distinguishing Site Characteristics, My Soil Type Is
with open('../csvs/soil_survey.csv', 'r') as csvfile:  # 'r' is for read
    reader = csv.DictReader(csvfile)    # dict v. regular: name instead of idx
    for row in reader:
        # Strip ``Collected`` so that it is in the correct format
        date = row['Collected'].strip('MonTuesWdhurFiSat(Aly), ')

        # Create foreign key relation between datasheet and site
        site = Site.objects.get(site_name=row['Stream/Site name'])
        site_id = site.id

        if row['Landscape Position'] == 'Large Flat Area':
            landscape_pos = 'large_flat'
        else:
            landscape_pos = row['Landscape Position'].lower().replace(
                ' ', '_')

        cover_type = row['Cover Type'].lower().replace(' ', '_')

        land_use = row['Land Use'].lower()

        dist = row['Distance From Stream'].strip(' ').lower()
        if 'feet' in dist or 'ft' in dist:
            if 'inches' in dist:
                dist = dist.strip('inches')
                dist_feet = float(dist[:dist.index('f')])
                dist_inches = float(dist[dist.index('t')+1:])
                dist = dist_inches / 12 + dist_feet
            else:
                dist = float(dist.strip('feet'))
            dist = feet_to_meters(dist)
        elif 'to' in dist:
            dist_low = float(dist[:dist.index('t')])
            dist_high = float(dist[(dist.index('o')+1):])
            dist = (dist_low + dist_high) / 2
            dist = feet_to_meters(dist)
        elif 'meters' in dist:
            dist = float(dist.strip('meters'))
        elif dist == '':
            dist = None
        else:
            dist = feet_to_meters(float(dist))

        site_char = row['Distinguishing Site Characteristics']

        soil_type = row['My Soil Type Is'].lower().replace(' ', '_')
        if soil_type[-1] == ')':
            soil_type = soil_type[:-4]
        types = ['sand', 'loamy_sand', 'silt_loam', 'loam', 'clay_loam',
                 'light_clay', 'heavy_clay', 'n/a']
        for s_type in types:
            if soil_type == s_type:         # if soil type matches valid,
                break                       # cancel loop
            elif soil_type == 'not_our_system':
                soil_type = 'n/a'
                break
        else:
            soil_type = 'other'             # assign "other"

        weather = ''

        # TODO: Find actual school from outside the CSV
        school = None

        soil = Soil_Survey.objects.update_or_create(
            date=date, site_id=site_id, landscape_pos=landscape_pos,
            cover_type=cover_type, land_use=land_use, distance=dist,
            site_char=site_char, soil_type=soil_type, weather=weather,
            school=school
        )

csvfile.close()
print('Soil survey data loaded.')
