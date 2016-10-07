#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/opt/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Site  # NOQA
from streamwebs.models import Macroinvertebrates  # NOQA

# Site, school, Collected, Post date, Time spent, # of peeps,
# Water Type (riffle/pool), caddisfly, mayfly, riffle beetle, stonefly,
# water penny, dobsonfly, clam/mussel, crane fly, crayfish, damselfly,
# dragonfly, scud, fishfly, adlerfly, mite, aquatic worm, blackfly, leech,
# midge, snail, mosquito

with open('../csvs/macros.csv', 'r') as csvfile:
    macroreader = csv.reader(csvfile)
    for row in macroreader:
        if row[0] != 'Stream/Site name':  # Skip the header
            macros = Macroinvertebrates()

            # Strip ``Collected date`` so that's in the correct format
            dt = row[2].strip('MonTuesWdhurFiSat(Aly), ')
            macros.date_time = dt

            # Apparently, Drupal will accept any value as valid... --> parse it
            ts = row[4].strip('hrminutes. ')
            if (ts == 'NA' or ts == ''):
                macros.time_spent = None
            elif ts == '20-30':
                macros.time_spent = 25
            else:   # In the SW model, we expect a positive integer...
                macros.time_spent = round(float(ts))

            if (row[5] == 'NA' or row[5] == 'UNK' or row[5] == ''):
                macros.num_people = None
            else:
                macros.num_people = row[5]

            # Determine water/type here
            if row[6] == 'Riffle':
                macros.riffle = True
            elif row[6] == 'Pool':
                macros.pool = True
            else:
                macros.riffle = False
                macros.pool = False

            for i in range(7, 28):
                if row[i] == '':  # Convert '' -> 0
                    row[i] = 0

            # Sensitive
            macros.caddisfly = row[7]
            macros.mayfly = row[8]
            macros.riffle_beetle = row[9]
            macros.stonefly = row[10]
            macros.water_penny = row[11]
            macros.dobsonfly = row[12]
            for i in range(7, 12+1):
                macros.sensitive_total += int(row[i])*3
            

            # Somewhat Sensitive
            macros.clam_or_mussel = row[13]
            macros.crane_fly = row[14]
            macros.crayfish = row[15]
            macros.damselfly = row[16]
            macros.dragonfly = row[17]
            macros.scud = row[18]
            macros.fishfly = row[19]
            macros.alderfly = row[20]
            macros.mite = row[21]
            for i in range(13, 21+1):
                macros.somewhat_sensitive_total += int(row[i])*2

            # Tolerant
            macros.aquatic_worm = row[22]
            macros.blackfly = row[23]
            macros.leech = row[24]
            macros.midge = row[25]
            macros.snail = row[26]
            macros.mosquito_larva = row[27]
            for i in range(22, 27+1):
                macros.tolerant_total += int(row[i])

            # Create the foreign key relation between datasheet and site
            site = Site.objects.get(site_name=row[0])
            macros.site_id = site.id

            macros.save()

print 'Data loaded.'
