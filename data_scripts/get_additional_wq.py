#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/opt/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import WQ_Sample  # NOQA


# Conductivity, Type, Nid, delta
with open('../csvs/wq_csvs/small/conduct.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if 'Conductivity' not in row[0]:  # Skip the header
            # Search for matching Nid and sample
            conduct_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            conduct_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            conduct_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            conduct_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                conduct_1.conductivity = row[0]
            elif row[3] == '1':
                conduct_2.conductivity = row[0]
            elif row[3] == '2':
                conduct_3.conductivity = row[0]
            else:
                conduct_4.conductivity = row[0]

            conduct_1.save()
            conduct_2.save()
            conduct_3.save()
            conduct_4.save()

csvfile.close()

# Total Solids, Type, Nid, delta
with open('../csvs/wq_csvs/small/total_sol.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Total Solids (mg/L)':  # Skip the header
            # Search for matching Nid and sample
            total_solids_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            total_solids_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            total_solids_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            total_solids_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                total_solids_1.total_solids = row[0]
            elif row[3] == '1':
                total_solids_2.total_solids = row[0]
            elif row[3] == '2':
                total_solids_3.total_solids = row[0]
            else:
                total_solids_4.total_solids = row[0]

            total_solids_1.save()
            total_solids_2.save()
            total_solids_3.save()
            total_solids_4.save()

csvfile.close()

# BOD, Type, Nid, delta
with open('../csvs/wq_csvs/small/bod.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'BOD (mg/L)':  # Skip the header
            # Search for matching Nid and sample
            bod_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            bod_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            bod_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            bod_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                bod_1.bod = row[0]
            elif row[3] == '1':
                bod_2.bod = row[0]
            elif row[3] == '2':
                bod_3.bod = row[0]
            else:
                bod_4.bod = row[0]

            bod_1.save()
            bod_2.save()
            bod_3.save()
            bod_4.save()

csvfile.close()

# Ammonia, Type, Nid, delta
with open('../csvs/wq_csvs/small/ammonia.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Ammonia (mg/L)':  # Skip the header
            # Search for matching Nid and sample
            ammonia_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            ammonia_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            ammonia_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            ammonia_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                ammonia_1.ammonia = row[0]
            elif row[3] == '1':
                ammonia_2.ammonia = row[0]
            elif row[3] == '2':
                ammonia_3.ammonia = row[0]
            else:
                ammonia_4.ammonia = row[0]

            ammonia_1.save()
            ammonia_2.save()
            ammonia_3.save()
            ammonia_4.save()

csvfile.close()

# Nitrite, Type, Nid, delta
with open('../csvs/wq_csvs/small/nitrite.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nitrite (mg/L)':  # Skip the header
            # Search for matching Nid and sample
            nitrite_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            nitrite_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            nitrite_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            nitrite_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                nitrite_1.nitrite = row[0]
            elif row[3] == '1':
                nitrite_2.nitrite = row[0]
            elif row[3] == '2':
                nitrite_3.nitrite = row[0]
            else:
                nitrite_4.nitrite = row[0]

            nitrite_1.save()
            nitrite_2.save()
            nitrite_3.save()
            nitrite_4.save()

csvfile.close()

# Nitrate, Type, Nid, delta
with open('../csvs/wq_csvs/small/nitrate.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nitrate (mg/L)':  # Skip the header
            # Search for matching Nid and sample
            nitrate_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            nitrate_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            nitrate_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            nitrate_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                nitrate_1.nitrate = row[0]
            elif row[3] == '1':
                nitrate_2.nitrate = row[0]
            elif row[3] == '2':
                nitrate_3.nitrate = row[0]
            else:
                nitrate_4.nitrate = row[0]

            nitrate_1.save()
            nitrate_2.save()
            nitrate_3.save()
            nitrate_4.save()

csvfile.close()

# Phosphates, Type, Nid, delta
with open('../csvs/wq_csvs/small/phosphates.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Phosphates (mg/L)':  # Skip the header
            # Search for matching Nid and sample
            phosphates_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            phosphates_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            phosphates_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            phosphates_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                phosphates_1.phosphates = row[0]
            elif row[3] == '1':
                phosphates_2.phosphates = row[0]
            elif row[3] == '2':
                phosphates_3.phosphates = row[0]
            else:
                phosphates_4.phosphates = row[0]

            phosphates_1.save()
            phosphates_2.save()
            phosphates_3.save()
            phosphates_4.save()

csvfile.close()

# Fecal Coliform, Type, Nid, delta
with open('../csvs/wq_csvs/small/fecal_col.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Fecal Coliform (CFU/100mL)':  # Skip the header
            # Search for matching Nid and sample
            fecal_col_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            fecal_col_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            fecal_col_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            fecal_col_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                fecal_col_1.fecal_coliform = row[0]
            elif row[3] == '1':
                fecal_col_2.fecal_coliform = row[0]
            elif row[3] == '2':
                fecal_col_3.fecal_coliform = row[0]
            else:
                fecal_col_4.fecal_coliform = row[0]

            fecal_col_1.save()
            fecal_col_2.save()
            fecal_col_3.save()
            fecal_col_4.save()

csvfile.close()

print 'Loaded.'
