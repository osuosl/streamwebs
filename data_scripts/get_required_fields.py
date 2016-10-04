#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "/opt/streamwebs/streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Water_Quality  # NOQA
from streamwebs.models import WQ_Sample  # NOQA


# Water Temperature, Type, Nid, Water Temp (delta)
with open('../csvs/wq_csvs/WQ_water_temp.csv', 'r') as csvfile:
    waterreader = csv.DictReader(csvfile)
    for row in waterreader:
        # if row[0] != 'Water Temperature':  # Skip the header
            water_temp = WQ_Sample()

            # Check delta values and assign sample numbers
            if row['Delta'] == '':
                water_temp.sample = 1
            elif row['Delta'] == '1':
                water_temp.sample = 2
            elif row['Delta'] == '2':
                water_temp.sample = 3
            else:
                water_temp.sample = 4

            # Set to null if value is not specified
            if row['Water Temperature'] == '':
                row['Water Temperature'] = None

            water_temp.water_temperature = row['Water Temperature']
            water_temp.nid = row['Nid']

            # Create foreign key relation between samples and parent datasheet
            waterq = Water_Quality.objects.get(nid=row['Nid'])
            water_temp.water_quality_id = waterq.id

            water_temp.save()

csvfile.close()
print 'Water temperature loaded.'

# Stream/Site name, Type, Nid, Air Temperature, Air Temp (delta)
with open('../csvs/wq_csvs/WQ_air_temp.csv', 'r') as csvfile:
    airreader = csv.reader(csvfile)
    for row in airreader:
        if row[0] != 'Stream/Site name':  # Skip the header
            # Search for matching Nid and sample
            air_temp_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            air_temp_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            air_temp_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            air_temp_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[3] == '':
                row[3] = None

            if row[4] == '':
                air_temp_1.air_temperature = row[3]
            elif row[4] == '1':
                air_temp_2.air_temperature = row[3]
            elif row[4] == '2':
                air_temp_3.air_temperature = row[3]
            else:
                air_temp_4.air_temperature = row[3]

            air_temp_1.save()
            air_temp_2.save()
            air_temp_3.save()
            air_temp_4.save()

csvfile.close()
print 'Air temperature loaded.'

# Dissolved Oxygen, Type, Nid, D_Oxygen (delta)
with open('../csvs/wq_csvs/WQ_oxygen.csv', 'r') as csvfile:
    oxygenreader = csv.reader(csvfile)
    for row in oxygenreader:
        if row[0] != 'Dissolved Oxygen (mg/L)':  # Skip the header
            # Search for matching Nid and sample
            oxygen_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            oxygen_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            oxygen_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            oxygen_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                oxygen_1.dissolved_oxygen = row[0]
            elif row[3] == '1':
                oxygen_2.dissolved_oxygen = row[0]
            elif row[3] == '2':
                oxygen_3.dissolved_oxygen = row[0]
            else:
                oxygen_4.dissolved_oxygen = row[0]

            oxygen_1.save()
            oxygen_2.save()
            oxygen_3.save()
            oxygen_4.save()

csvfile.close()
print 'Dissolved oxygen loaded.'

# pH, Type, Nid, pH (delta)
with open('../csvs/wq_csvs/WQ_pH.csv', 'r') as csvfile:
    pHreader = csv.reader(csvfile)
    for row in pHreader:
        if row[0] != 'pH':  # Skip the header
            # Search for matching Nid and sample
            pH_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            pH_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            pH_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            pH_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                pH_1.pH = row[0]
            elif row[3] == '1':
                pH_2.pH = row[0]
            elif row[3] == '2':
                pH_3.pH = row[0]
            else:
                pH_4.pH = row[0]

            pH_1.save()
            pH_2.save()
            pH_3.save()
            pH_4.save()

csvfile.close()
print 'pH loaded.'

# Turbidity, Type, Nid, Turbidity (delta)
with open('../csvs/wq_csvs/WQ_turbidity.csv', 'r') as csvfile:
    turbidreader = csv.reader(csvfile)
    for row in turbidreader:
        if row[0] != 'Turbidity (NTU)':  # Skip the header
            # Search for matching Nid and sample
            turbidity_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            turbidity_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            turbidity_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            turbidity_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                turbidity_1.turbidity = row[0]
            elif row[3] == '1':
                turbidity_2.turbidity = row[0]
            elif row[3] == '2':
                turbidity_3.turbidity = row[0]
            else:
                turbidity_4.turbidity = row[0]

            turbidity_1.save()
            turbidity_2.save()
            turbidity_3.save()
            turbidity_4.save()

csvfile.close()
print 'Turbidity loaded.'

# Salinity, Type, Nid, salt (delta)
with open('../csvs/wq_csvs/WQ_salinity.csv', 'r') as csvfile:
    saltreader = csv.reader(csvfile)
    for row in saltreader:
        if row[0] != 'Salinity (PSU) PPT':  # Skip the header
            # Search for matching Nid and sample
            salt_1 = WQ_Sample.objects.get(nid=row[2], sample=1)
            salt_2 = WQ_Sample.objects.get(nid=row[2], sample=2)
            salt_3 = WQ_Sample.objects.get(nid=row[2], sample=3)
            salt_4 = WQ_Sample.objects.get(nid=row[2], sample=4)

            # Set to null if value is not specified
            if row[0] == '':
                row[0] = None

            if row[3] == '':
                salt_1.salinity = row[0]
            elif row[3] == '1':
                salt_2.salinity = row[0]
            elif row[3] == '2':
                salt_3.salinity = row[0]
            else:
                salt_4.salinity = row[0]

            salt_1.save()
            salt_2.save()
            salt_3.save()
            salt_4.save()

csvfile.close()
print 'Salinity loaded.'
