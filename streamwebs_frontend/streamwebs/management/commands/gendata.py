from django.core.management.base import BaseCommand
from streamwebs.models import Site, Water_Quality, WQ_Sample

from datetime import date
from random import randint, uniform


class Command(BaseCommand):
    help = 'Generates a bunch of random, fake data for testing with'

    def add_arguments(self, parser):
        parser.add_argument(
            'type',
            action='store',
            nargs='?',
            default='all',
            choices=['wq', 'macros', 'cc', 'transect', 'soil', 'all'],
            help='The type of data to generate. All creates one site with '
                 'all types.'

        )

    def handle(self, *args, **options):
        s = None
        type = options['type']
        if type == 'wq':
            print('Creating site `wq-test`...')
            s = Site.objects.create(site_name='Water Quality Test Data',
                                    site_slug='wq-test',
                                    location='POINT(-120 45)')
        elif type == 'macros':
            print('Creating site `macro-test`...')
            s = Site.objects.create(site_name='Macroinvertebrate Test Data',
                                    site_slug='macro-test',
                                    location='POINT(-120 45)')
        elif type == 'cc':
            print('Creating site `cc-test`...')
            s = Site.objects.create(site_name='Canopy Cover Test Data',
                                    site_slug='cc-test',
                                    location='POINT(-120 45)')
        elif type == 'transect':
            print('Creating site `transect-test`...')
            s = Site.objects.create(site_name='Riparian Transect Test Data',
                                    site_slug='transect-test',
                                    location='POINT(-120 45)')
        elif type == 'soil':
            print('Creating site `soil-test`...')
            s = Site.objects.create(site_name='Soil Survey Test Data',
                                    site_slug='soil-test',
                                    location='POINT(-120 45)')
        elif type == 'all':
            print('Creating site `data-test`...')
            s = Site.objects.create(site_name='Generated Test Data',
                                    site_slug='data-test',
                                    location='POINT(-120 45)')
        s.save()

        if type == 'wq' or type == 'all':
            print('Generating Water Quality data...')
            for month in range(1, 13):
                for i in range(randint(50, 100)):
                    wq = Water_Quality.objects.create(site=s,
                                                      date=date(2017, month, 1),
                                                      DEQ_dq_level='C',
                                                      school=None,
                                                      latitude=-120,
                                                      longitude=45,
                                                      fish_present='True',
                                                      live_fish=3,
                                                      dead_fish=2,
                                                      water_temp_unit='Celsius',
                                                      air_temp_unit='Celsius')
                    wq.save()

                    for n in range(4):
                        ammonia = uniform(1, 10)
                        nitrite = uniform(1, 10)
                        nitrate = uniform(1, 10)
                        phosphates = uniform(1, 10)
                        total_solids = ammonia + nitrite + nitrate + phosphates
                        sample = WQ_Sample\
                            .objects.create(water_quality=wq,
                                            sample=n,
                                            water_temp_tool='Manual',
                                            air_temp_tool='Manual',
                                            oxygen_tool='Manual',
                                            pH_tool='Manual',
                                            turbid_tool='Manual',
                                            salt_tool='Manual',
                                            water_temperature=uniform(30, 60),
                                            air_temperature=uniform(30, 60),
                                            dissolved_oxygen=uniform(1, 30),
                                            pH=uniform(1, 14),
                                            turbidity=uniform(1, 10),
                                            salinity=uniform(1, 5),
                                            conductivity=uniform(10, 20),
                                            bod=uniform(1, 10),
                                            fecal_coliform=uniform(1, 10),
                                            ammonia=ammonia,
                                            nitrite=nitrite,
                                            nitrate=nitrate,
                                            phosphates=phosphates,
                                            total_solids=total_solids)
                        sample.save()

        if type == 'macros' or type == 'all':
            print('Generating Macroinvertebrate data...')

        if type == 'cc' or type == 'all':
            print('Generating Canopy Cover data...')

        if type == 'transect' or type == 'all':
            print('Generating Riparian Transect data...')

        if type == 'soil' or type == 'all':
            print('Generating Soil Survey data...')

        print('Data generated.')
