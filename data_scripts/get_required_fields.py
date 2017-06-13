#!/usr/bin/env python

import os
import sys
import csv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamwebs_frontend.settings")
proj_path = "../streamwebs_frontend/"
sys.path.append(proj_path)
application = get_wsgi_application()

from streamwebs.models import Water_Quality  # NOQA
from streamwebs.models import WQ_Sample  # NOQA


if os.path.isdir("../streamwebs_frontend/sw_data/"):
    datapath = '../sw_data/wq_csvs/'
else:
    datapath = '../csvs/wq_csvs/'


watertemp = datapath + 'WQ_water_temp.csv'
airtemp = datapath + 'WQ_air_temp.csv'
oxygen = datapath + 'WQ_oxygen.csv'
pH = datapath + 'WQ_pH.csv'
turbidity = datapath + 'WQ_turbidity.csv'
salinity = datapath + 'WQ_salinity.csv'


# Water Temperature, Type, Nid, Water Temp (delta)
with open(watertemp, 'r') as csvfile:
    waterreader = csv.DictReader(csvfile)
    for row in waterreader:
            # Check delta values and assign sample numbers
            if row['Delta'] == '':
                sample = 1
            elif row['Delta'] == '1':
                sample = 2
            elif row['Delta'] == '2':
                sample = 3
            else:
                sample = 4

            if row['Water Temperature'] != '':
                water_temperature = row['Water Temperature']
            else:
                water_temperature = None

            nid = row['Nid']

            # Create foreign key relation between samples and parent datasheet
            waterq = Water_Quality.objects.get(nid=row['Nid'])

            # Create new entry if datasheet sample does not yet exist
            water_temp = WQ_Sample.objects.update_or_create(
                sample=sample, water_temperature=water_temperature, nid=nid,
                water_quality_id=waterq.id
            )

csvfile.close()
print 'Water temperature loaded.'

# Stream/Site name, Type, Nid, Air Temperature, Air Temp (delta)
with open(airtemp, 'r') as csvfile:
    airreader = csv.DictReader(csvfile)
    for row in airreader:
            # Skip the row if no value is specified
            if row['Air Temperature'] != '':
                if WQ_Sample.objects.filter(nid=row['Nid']).exists():
                    if row['Delta'] == '':
                        # Search for matching Nid and sample
                        air_temp_1 = WQ_Sample.objects.get(
                            nid=row['Nid'], sample=1)
                        air_temp_1.air_temperature = row['Air Temperature']
                        air_temp_1.save()
                    elif row['Delta'] == '1':
                        air_temp_2 = WQ_Sample.objects.get(
                            nid=row['Nid'], sample=2)
                        air_temp_2.air_temperature = row['Air Temperature']
                        air_temp_2.save()
                    elif row['Delta'] == '2':
                        air_temp_3 = WQ_Sample.objects.get(
                            nid=row['Nid'], sample=3)
                        air_temp_3.air_temperature = row['Air Temperature']
                        air_temp_3.save()
                    else:
                        air_temp_4 = WQ_Sample.objects.get(
                            nid=row['Nid'], sample=4)
                        air_temp_4.air_temperature = row['Air Temperature']
                        air_temp_4.save()
                else:
                    if row['Delta'] == '':
                        sample = 1
                    elif row['Delta'] == '1':
                        sample = 2
                    elif row['Delta'] == '2':
                        sample = 3
                    else:
                        sample = 4
    
                    if row['Air Temperature'] != '':
                        air_temperature = row['Air Temperature']
                    else:
                        air_temperature = None
    
                    nid = row['Nid']
    
                    # Create foreign key relation
                    waterq = Water_Quality.objects.get(nid=row['Nid'])
 
                    # Create new entry if datasheet sample does not yet exist
                    air_temp = WQ_Sample.objects.update_or_create(
                        sample=sample, air_temperature=air_temperature,
                        nid=nid, water_quality_id=waterq.id
                    )

csvfile.close()
print 'Air temperature loaded.'

# Dissolved Oxygen, Type, Nid, D_Oxygen (delta)
with open(oxygen, 'r') as csvfile:
    oxygenreader = csv.DictReader(csvfile)
    for row in oxygenreader:
            # Skip row if no value is specified
            if row['Dissolved Oxygen (mg/L)'] != '':
                if row['Delta'] == '':
                    oxygen_1 = WQ_Sample.objects.get(nid=row['Nid'], sample=1)
                    oxygen_1.dissolved_oxygen = row['Dissolved Oxygen (mg/L)']
                    oxygen_1.save()
                elif row['Delta'] == '1':
                    oxygen_2 = WQ_Sample.objects.get(nid=row['Nid'], sample=2)
                    oxygen_2.dissolved_oxygen = row['Dissolved Oxygen (mg/L)']
                    oxygen_2.save()
                elif row['Delta'] == '2':
                    oxygen_3 = WQ_Sample.objects.get(nid=row['Nid'], sample=3)
                    oxygen_3.dissolved_oxygen = row['Dissolved Oxygen (mg/L)']
                    oxygen_3.save()
                else:
                    oxygen_4 = WQ_Sample.objects.get(nid=row['Nid'], sample=4)
                    oxygen_4.dissolved_oxygen = row['Dissolved Oxygen (mg/L)']
                    oxygen_4.save()

csvfile.close()
print 'Dissolved oxygen loaded.'

# pH, Type, Nid, pH (delta)
with open(pH, 'r') as csvfile:
    pHreader = csv.DictReader(csvfile)
    for row in pHreader:
            # Skip row if value is not specified
            if row['pH'] != '':
                if row['Delta'] == '':
                    pH_1 = WQ_Sample.objects.get(nid=row['Nid'], sample=1)
                    pH_1.pH = row['pH']
                    pH_1.save()
                elif row['Delta'] == '1':
                    pH_2 = WQ_Sample.objects.get(nid=row['Nid'], sample=2)
                    pH_2.pH = row['pH']
                    pH_2.save()
                elif row['Delta'] == '2':
                    pH_3 = WQ_Sample.objects.get(nid=row['Nid'], sample=3)
                    pH_3.pH = row['pH']
                    pH_3.save()
                else:
                    pH_4 = WQ_Sample.objects.get(nid=row['Nid'], sample=4)
                    pH_4.pH = row['pH']
                    pH_4.save()

csvfile.close()
print 'pH loaded.'

# Turbidity, Type, Nid, Turbidity (delta)
with open(turbidity, 'r') as csvfile:
    turbidreader = csv.DictReader(csvfile)
    for row in turbidreader:
            # Skip row if value is not specified
            if row['Turbidity (NTU)'] != '':
                if row['Delta'] == '':
                    turbidity_1 = WQ_Sample.objects.get(
                        nid=row['Nid'], sample=1)
                    turbidity_1.turbidity = row['Turbidity (NTU)']
                    turbidity_1.save()
                elif row['Delta'] == '1':
                    turbidity_2 = WQ_Sample.objects.get(
                        nid=row['Nid'], sample=2)
                    turbidity_2.turbidity = row['Turbidity (NTU)']
                    turbidity_2.save()
                elif row['Delta'] == '2':
                    turbidity_3 = WQ_Sample.objects.get(
                        nid=row['Nid'], sample=3)
                    turbidity_3.turbidity = row['Turbidity (NTU)']
                    turbidity_3.save()
                else:
                    turbidity_4 = WQ_Sample.objects.get(
                        nid=row['Nid'], sample=4)
                    turbidity_4.turbidity = row['Turbidity (NTU)']
                    turbidity_4.save()

csvfile.close()
print 'Turbidity loaded.'

# Salinity, Type, Nid, salt (delta)
with open(salinity, 'r') as csvfile:
    saltreader = csv.DictReader(csvfile)
    for row in saltreader:
            # Skip row if value is not specified
            if row['Salinity (PSU) PPT'] != '':
                if row['Delta'] == '':
                    salt_1 = WQ_Sample.objects.get(nid=row['Nid'], sample=1)
                    salt_1.salinity = row['Salinity (PSU) PPT']
                    salt_1.save()
                elif row['Delta'] == '1':
                    salt_2 = WQ_Sample.objects.get(nid=row['Nid'], sample=2)
                    salt_2.salinity = row['Salinity (PSU) PPT']
                    salt_2.save()
                elif row['Delta'] == '2':
                    salt_3 = WQ_Sample.objects.get(nid=row['Nid'], sample=3)
                    salt_3.salinity = row['Salinity (PSU) PPT']
                    salt_3.save()
                else:
                    salt_4 = WQ_Sample.objects.get(nid=row['Nid'], sample=4)
                    salt_4.salinity = row['Salinity (PSU) PPT']
                    salt_4.save()

csvfile.close()
print 'Salinity loaded.'
