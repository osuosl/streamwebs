#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import Macroinvertebrates  # NOQA


if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datafile = '../sw_data/macros.csv'
else:
    datafile = '../csvs/macros.csv'


# Site, school, Collected, Post date, Time spent, # of peeps,
# Water Type (riffle/pool), caddisfly, mayfly, riffle beetle, stonefly,
# water penny, dobsonfly, clam/mussel, crane fly, crayfish, damselfly,
# dragonfly, scud, fishfly, adlerfly, mite, aquatic worm, blackfly, leech,
# midge, snail, mosquito

with open(datafile, 'r') as csvfile:
    macroreader = csv.reader(csvfile)
    for row in macroreader:
        if row[0] != 'Stream/Site name':  # Skip the header
            # Strip ``Collected date`` so that's in the correct format
            dt = row[2].strip('MonTuesWdhurFiSat(Aly), ')
            date_time = dt

            # Apparently, Drupal will accept any value as valid... --> parse it
            ts = row[4].strip('hrminutes. ')
            if (ts == 'NA' or ts == ''):
                time_spent = None
            elif ts == '20-30':
                time_spent = 25
            else:   # In the SW model, we expect a positive integer...
                time_spent = round(float(ts))

            if (row[5] == 'NA' or row[5] == 'UNK' or row[5] == ''):
                num_people = None
            else:
                num_people = row[5]

            # Determine water/type here
            if row[6] == 'Riffle':
                water_type = 'riff'
            elif row[6] == 'Pool':
                water_type = 'pool'
            else:
                water_type = None

            for i in range(7, 28):
                if row[i] == '':  # Convert '' -> 0
                    row[i] = 0

            # Sensitive
            caddisfly = row[7]
            mayfly = row[8]
            riffle_beetle = row[9]
            stonefly = row[10]
            water_penny = row[11]
            dobsonfly = row[12]

            # Somewhat Sensitive
            clam_or_mussel = row[13]
            crane_fly = row[14]
            crayfish = row[15]
            damselfly = row[16]
            dragonfly = row[17]
            scud = row[18]
            fishfly = row[19]
            alderfly = row[20]
            mite = row[21]

            # Tolerant
            aquatic_worm = row[22]
            blackfly = row[23]
            leech = row[24]
            midge = row[25]
            snail = row[26]
            mosquito_larva = row[27]

            uid = row[28]

            # Create the foreign key relation between datasheet and site
            site = Site.objects.get(site_name=row[0])
            site_id = site.id

            # Create new macro entry if it DNE
            macros = Macroinvertebrates.objects.update_or_create(
                date_time=date_time, time_spent=time_spent,
                num_people=num_people, water_type=water_type,
                caddisfly=caddisfly, mayfly=mayfly,
                riffle_beetle=riffle_beetle, stonefly=stonefly,
                water_penny=water_penny, dobsonfly=dobsonfly,
                clam_or_mussel=clam_or_mussel, crane_fly=crane_fly,
                crayfish=crayfish, damselfly=damselfly, dragonfly=dragonfly,
                scud=scud, fishfly=fishfly, alderfly=alderfly, mite=mite,
                aquatic_worm=aquatic_worm, blackfly=blackfly, leech=leech,
                midge=midge, snail=snail, mosquito_larva=mosquito_larva,
                site_id=site_id, uid=uid
            )

print 'Macroinvertebrates loaded.'
