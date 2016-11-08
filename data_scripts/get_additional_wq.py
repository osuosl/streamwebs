#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import WQ_Sample  # NOQA


if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datapath = '../sw_data/wq_csvs/'
else:
    datapath = '../csvs/wq_csvs/'


conductivity = datapath + 'WQ_conductivity.csv'
total_solids = datapath + 'WQ_total_solids.csv'
bod_data = datapath + 'WQ_bod.csv'
ammonia_data = datapath + 'WQ_ammonia.csv'
nitrite_data = datapath + 'WQ_nitrite.csv'
nitrate_data = datapath + 'WQ_nitrate.csv'
phosphate_data = datapath + 'WQ_phosphates.csv'
fecal_coliform = datapath + 'WQ_fecal_col.csv'

# Conductivity, Type, Nid, delta
with open(conductivity, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if 'Conductivity' not in row[0]:  # Skip the header
            # Skip row  if value is not specified
            if row[0] != '':
                if row[3] == '':
                    conduct_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
                    conduct_1.conductivity = row[0]
                    conduct_1.save()
                elif row[3] == '1':
                    conduct_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
                    conduct_2.conductivity = row[0]
                    conduct_2.save()
                elif row[3] == '2':
                    conduct_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
                    conduct_3.conductivity = row[0]
                    conduct_3.save()
                else:
                    conduct_4 = WQ_Sample.objects.get(nid=row[2], sample=4)
                    conduct_4.conductivity = row[0]
                    conduct_4.save()

csvfile.close()
print 'Conductivity loaded.'

# Total Solids, Type, Nid, delta
with open(total_solids, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Total Solids (mg/L)':  # Skip the header
            if row[0] != '':
                if row[3] == '':
                    total_solids_1 =\
                         WQ_Sample.objects.get(nid=row[2], sample=1)
                    total_solids_1.total_solids = row[0]
                    total_solids_1.save()
                elif row[3] == '1':
                    total_solids_2 =\
                         WQ_Sample.objects.get(nid=row[2], sample=2)
                    total_solids_2.total_solids = row[0]
                    total_solids_2.save()
                elif row[3] == '2':
                    total_solids_3 =\
                        WQ_Sample.objects.get(nid=row[2], sample=3)
                    total_solids_3.total_solids = row[0]
                    total_solids_3.save()
                else:
                    total_solids_4 =\
                        WQ_Sample.objects.get(nid=row[2], sample=4)
                    total_solids_4.total_solids = row[0]
                    total_solids_4.save()

csvfile.close()
print 'Total solids loaded.'

# BOD, Type, Nid, delta
with open(bod_data, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'BOD (mg/L)':  # Skip the header
            if row[0] != '':
                if row[3] == '':
                    bod_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
                    bod_1.bod = row[0]
                    bod_1.save()
                elif row[3] == '1':
                    bod_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
                    bod_2.bod = row[0]
                    bod_2.save()
                elif row[3] == '2':
                    bod_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
                    bod_3.bod = row[0]
                    bod_3.save()
                else:
                    bod_4 = WQ_Sample.objects.get(nid=row[2], sample=4)
                    bod_4.bod = row[0]
                    bod_4.save()

csvfile.close()
print 'BOD loaded.'

# Ammonia, Type, Nid, delta
with open(ammonia_data, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Ammonia (mg/L)':  # Skip the header
            if row[0] != '':
                if row[3] == '':
                    ammonia_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
                    ammonia_1.ammonia = row[0]
                    ammonia_1.save()
                elif row[3] == '1':
                    ammonia_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
                    ammonia_2.ammonia = row[0]
                    ammonia_2.save()
                elif row[3] == '2':
                    ammonia_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
                    ammonia_3.ammonia = row[0]
                    ammonia_3.save()
                else:
                    ammonia_4 = WQ_Sample.objects.get(nid=row[2], sample=4)
                    ammonia_4.ammonia = row[0]
                    ammonia_4.save()

csvfile.close()
print 'Ammonia loaded.'

# Nitrite, Type, Nid, delta
with open(nitrite_data, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nitrite (mg/L)':  # Skip the header
            if row[0] != '':
                if row[3] == '':
                    nitrite_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
                    nitrite_1.nitrite = row[0]
                    nitrite_1.save()
                elif row[3] == '1':
                    nitrite_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
                    nitrite_2.nitrite = row[0]
                    nitrite_2.save()
                elif row[3] == '2':
                    nitrite_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
                    nitrite_3.nitrite = row[0]
                    nitrite_3.save()
                else:
                    nitrite_4 = WQ_Sample.objects.get(nid=row[2], sample=4)
                    nitrite_4.nitrite = row[0]
                    nitrite_4.save()

csvfile.close()
print 'Nitrite loaded.'

# Nitrate, Type, Nid, delta
with open(nitrate_data, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Nitrate (mg/L)':  # Skip the header
            if row[0] != '':
                if row[3] == '':
                    nitrate_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
                    nitrate_1.nitrate = row[0]
                    nitrate_1.save()
                elif row[3] == '1':
                    nitrate_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
                    nitrate_2.nitrate = row[0]
                    nitrate_2.save()
                elif row[3] == '2':
                    nitrate_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
                    nitrate_3.nitrate = row[0]
                    nitrate_3.save()
                else:
                    nitrate_4 = WQ_Sample.objects.get(nid=row[2], sample=4)
                    nitrate_4.nitrate = row[0]
                    nitrate_4.save()

csvfile.close()
print 'Nitrate loaded.'

# Phosphates, Type, Nid, delta
with open(phosphate_data, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Phosphates (mg/L)':  # Skip the header
            if row[0] != '':
                if row[3] == '':
                    phosphates_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
                    phosphates_1.phosphates = row[0]
                    phosphates_1.save()
                elif row[3] == '1':
                    phosphates_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
                    phosphates_2.phosphates = row[0]
                    phosphates_2.save()
                elif row[3] == '2':
                    phosphates_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
                    phosphates_3.phosphates = row[0]
                    phosphates_3.save()
                else:
                    phosphates_4 = WQ_Sample.objects.get(nid=row[2], sample=4)
                    phosphates_4.phosphates = row[0]
                    phosphates_4.save()

csvfile.close()
print 'Phophates loaded.'

# Fecal Coliform, Type, Nid, delta
with open(fecal_coliform, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Fecal Coliform (CFU/100mL)':  # Skip the header
            if row[0] != '':
                if row[3] == '':
                    fecal_col_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
                    fecal_col_1.fecal_coliform = row[0]
                    fecal_col_1.save()
                elif row[3] == '1':
                    fecal_col_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
                    fecal_col_2.fecal_coliform = row[0]
                    fecal_col_2.save()
                elif row[3] == '2':
                    fecal_col_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
                    fecal_col_3.fecal_coliform = row[0]
                    fecal_col_3.save()
                else:
                    fecal_col_4 = WQ_Sample.objects.get(nid=row[2], sample=4)
                    fecal_col_4.fecal_coliform = row[0]
                    fecal_col_4.save()

csvfile.close()
print 'Fecal coliform loaded.'
