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
from streamwebs.models import WQ_Sample  # NOQA


# Water Temp 1, 2, 4, 3
# Air Temp 1, 2, 3, 4 
# Dissolved Oxygen... etc.

with open('../csvs/wq_csvs/small/tools.csv', 'r') as csvfile:
    toolreader = csv.reader(csvfile)
    for row in toolreader:
        if row[0] != 'Equipment type - Water Temp. sample 1':  # Skip header
            # If tool is not specified, store as None, else fix capitalization
            for i in range(0, 24):
                if row[i] == '':
                    row[i] = None
                elif row[i] == 'manual':
                    row[i] = 'Manual'
                elif row[i] == 'vernier':
                    row[i] = 'Vernier'

            # Search for matching nid and sample number
            tool_1 = WQ_Sample.objects.get(nid=row[24], sample=1)
            tool_2 = WQ_Sample.objects.get(nid=row[24], sample=2)
            tool_3 = WQ_Sample.objects.get(nid=row[24], sample=3)
            tool_4 = WQ_Sample.objects.get(nid=row[24], sample=4)

            # If nid matches, set tool
            if (int(row[24]) == tool_1.nid):
                tool_1.water_temp_tool = row[0]
                tool_1.air_temp_tool = row[4]
                tool_1.oxygen_tool = row[8]
                tool_1.ph_tool = row[12]
                tool_1.turbid_tool = row[16]
                tool_1.salt_tool = row[20]

            if (int(row[24]) == tool_2.nid):
                tool_2.water_temp_tool = row[1]
                tool_2.air_temp_tool = row[5]
                tool_2.oxygen_tool = row[9]
                tool_2.ph_tool = row[13]
                tool_2.turbid_tool = row[17]
                tool_2.salt_tool = row[21]

            if (int(row[24]) == tool_3.nid):
                tool_3.water_temp_tool = row[2]
                tool_3.air_temp_tool = row[6]
                tool_3.oxygen_tool = row[10]
                tool_3.ph_tool = row[14]
                tool_3.turbid_tool = row[18]
                tool_3.salt_tool = row[22]

            if (int(row[24]) == tool_4.nid):
                tool_4.water_temp_tool = row[3]
                tool_4.air_temp_tool = row[7]
                tool_4.oxygen_tool = row[11]
                tool_4.ph_tool = row[15]
                tool_4.turbid_tool = row[19]
                tool_4.salt_tool = row[23]

            tool_1.save()
            tool_2.save()
            tool_3.save()
            tool_4.save()

csvfile.close()

print 'Measurement tools loaded.'
