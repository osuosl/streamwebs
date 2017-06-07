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
from streamwebs.models import Canopy_Cover  # NOQA


key_val_map = {
    '1': None,
    '2': None,
    '3': 0,  # A
    '4': 1,  # B
    '5': None,
    '6': None,
    '7': None,
    '8': 2,  # C
    '9': 3,  # D
    '10': 4,  # E
    '11': 5,  # F
    '12': None,
    '13': 6,  # G
    '14': 7,  # H
    '15': 8,  # I
    '16': 9,  # J
    '17': 10,  # K
    '18': 11,  # L
    '19': 12,  # M
    '20': 13,  # N
    '21': 14,  # O
    '22': 15,  # P
    '23': 16,  # Q
    '24': 17,  # R
    '25': None,
    '26': 18,  # S
    '27': 19,  # T
    '28': 20,  # U
    '29': 21,  # V
    '30': None,
    '31': None,
    '32': None,
    '33': 22,  # W
    '34': 23,  # X
    '35': None,
    '36': None
}

CCs = {}

directions = ['north', 'east', 'south', 'west']

for dir in directions:
    if os.path.isdir("../streamwebs_frontend/sw_data/"):
        datafile = '../sw_data/cc_' + dir + '.csv'
    else:
        datafile = '../csvs/cc_' + dir + '.csv'

    with open(datafile, 'r') as csvfile:
        sitereader = csv.DictReader(csvfile)
        cc = None
        count = 0
        for row in sitereader:
            if row[dir.capitalize()]:
                if row['Delta'] == '':
                    if row['Nid'] in CCs:
                        cc = CCs[row['Nid']]
                    else:
                        cc = Canopy_Cover()
                        cc.site = Site.objects.get(
                            site_name=row['Stream/Site name'].strip()
                        )
                        if row['Collected'][16] == '0' or \
                           row['Collected'][16] == '0' or \
                           row['Collected'][16] == '0':
                            cc.date_time = datetime.strptime(
                                row['Collected'],
                                "%a, %Y-%m-%d %H:%M"
                            )
                        else:
                            cc.date_time = datetime.strptime(
                                row['Collected'][0:15],
                                "%a, %Y-%m-%d"
                            )
                        cc.uid = row['Uid']

                    CCs[row['Nid']] = cc
                    count = 0

                if key_val_map[row[dir.capitalize()]] is not None:
                    count |= (1 << key_val_map[row[dir.capitalize()]])
                setattr(cc, dir + '_cc', count)
                CCs['Nid'] = cc

for cc in CCs.values():
    # Estimated cover = the sum of the number of bits set on each field
    cc.est_canopy_cover = \
        bin(cc.north_cc).count('1') + \
        bin(cc.east_cc).count('1') + \
        bin(cc.south_cc).count('1') + \
        bin(cc.west_cc).count('1')

    Canopy_Cover.objects.update_or_create(
        site=cc.site, school=None, date_time=cc.date_time, weather='',
        north_cc=cc.north_cc, east_cc=cc.east_cc, south_cc=cc.south_cc,
        west_cc=cc.west_cc, est_canopy_cover=cc.est_canopy_cover, uid=cc.uid
    )

print('Canopy Covers loaded.')
