from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Site
from streamwebs.models import Rip_Aqua_Survey
from streamwebs.models import Rip_Aqua_Survey_Plants
from streamwebs.models import Rip_Aqua_Survey_Wildlife

class RipAquaSurveyPlantTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'id': models.AutoField,
            'species': models.CharField,
            'significance': models.CharField,
        }
        self.optional_fields = {
            'species',
            'significance',
        }

class RipAquaSurveyWildLifeTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'id': models.AutoField,
            'track': models.CharField,
            'comments': models.CharField,
        }
        self.optional_fields = {
            'track',
            'comments',
        }

class RipAquaSurveyTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'id': models.AutoField,
            # Form header
            'user': models.ForeignKey,
            'date': models.DateField,
            'school': models.CharField,
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'weather': models.CharField,
            # Survey Area
            'stream_length': models.CharField,
            'riffle_count': models.CharField,
            'pool_count': models.CharField,
            # Substrate
            'silt': models.CharField,
            'sand': models.CharField,
            'gravel': models.CharField,
            'cobb;e': models.CharField,
            'boulders': models.CharField,
            'bedrock': models.CharField,
            # Instream Woody Debris
            'wood_debris_small': models.CharField,
            'wood_debris_med': models.CharField,
            'wood_debris_lrg': models.CharField,
            # Vegetation Types
            'conif_trees': models.CharField,
            'decid_trees': models.CharField,
            'shrubs': models.CharField,
            'small_plants': models.CharField,
            'ferns': models.CharField,
            'grasses': models.CharField,
            # Plants Identified
            'plants_1_id': models.CharField,
            'plants_2_id': models.CharField,
            'plants_3_id': models.CharField,
            'plants_4_id': models.CharField,
            'plants_5_id': models.CharField,
            'plants_6_id': models.CharField,
            # Wildlife & Birds Identified
            'wildlife_1_id': models.CharField,
            'wildlife_2_id': models.CharField,
            'wildlife_3_id': models.CharField,
            'wildlife_4_id': models.CharField,
            'wildlife_5_id': models.CharField,
            'wildlife_6_id': models.CharField,

        }
        self.optional_fields = {
           'comments',
           # Plants Identified
           'plants_1_id',
           'plants_2_id',
           'plants_3_id',
           'plants_4_id',
           'plants_5_id',
           'plants_6_id',
           # Wildlife & Birds Identified
           'wildlife_1_id',
           'wildlife_2_id',
           'wildlife_3_id',
           'wildlife_4_id',
           'wildlife_5_id',
           'wildlife_6_id',
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'rip_aqua_survey')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        model = Rip_Aqua_Survey
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in model._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        model = Rip_Aqua_Survey
        apps.get_model('streamwebs', model)
        for field in self.optional_fields:
            self.assertEqual(
                model._meta.get_field(field).blank, True)

    """
    def test_datasheet_ManyToOneSite(self):
        """Tests that a datasheet correctly corresponds to a specified site"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        sample_1 = WQ_Sample.objects.create_sample(35, 'Manual', 70,
                                                   'Manual', 6, 'Manual',
                                                   8.65, 'Vernier', 0.879,
                                                   'Manual', 8.8, 'Vernier',
                                                   15, 10, 7, 0.93,
                                                   2.1, 1.9, 14.5, 13)

        sample_2 = WQ_Sample.objects.create_sample(35, 'Vernier', 70,
                                                   'Vernier', 5, 'Vernier',
                                                   0.5, 'Manual', 8.79,
                                                   'Vernier', 8, 'Manual',
                                                   1, 0.10, 29, 0.93, 2.1,
                                                   2.0, 1.45, 10)

        sample_3 = WQ_Sample.objects.create_sample(25, 'Manual', 57,
                                                   'Vernier', 12, 'Manual',
                                                   8.45, 'Vernier', 0.87,
                                                   'Manual', 9.8, 'Vernier')

        sample_4 = WQ_Sample.objects.create_sample(45, 'Vernier', 89,
                                                   'Manual', 9, 'Vernier',
                                                   3.25, 'Vernier', 0.879,
                                                   'Manual', 8, 'Vernier',
                                                   0, 0, 0, 0, 2.5, 0, 0, 0)

        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp_unit='Fahrenheit',
                                              air_temp_unit='Fahrenheit',
                                              sample_1=sample_1,
                                              sample_2=sample_2,
                                              sample_3=sample_3,
                                              sample_4=sample_4,
                                              notes='Test data made')
        # Assert that site data matches the newly created test site
        self.assertEqual(waterq.site.site_name, 'test')
        self.assertEqual(waterq.site.site_type, 'some_type')
        self.assertEqual(waterq.site.site_slug, 'some_slug')

    def test_datasheet_SetSampleInfo(self):
        """Tests that a datasheet correctly corresponds to a specified
           measurement entry - required fields"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        sample_1 = WQ_Sample.objects.create_sample(35, 'Manual', 70,
                                                   'Manual', 6, 'Manual',
                                                   8.65, 'Vernier', 0.879,
                                                   'Manual', 8.8, 'Vernier',
                                                   15, 10, 7, 0.93,
                                                   2.1, 1.9, 14.5, 13)

        sample_2 = WQ_Sample.objects.create_sample(35, 'Vernier', 70,
                                                   'Vernier', 5, 'Vernier',
                                                   0.5, 'Manual', 8.79,
                                                   'Vernier', 8, 'Manual',
                                                   1, 0.10, 29, 0.93, 2.1,
                                                   2.0, 1.45, 10)

        sample_3 = WQ_Sample.objects.create_sample(25, 'Manual', 57,
                                                   'Vernier', 12, 'Manual',
                                                   8.45, 'Vernier', 0.87,
                                                   'Manual', 9.8, 'Vernier')

        sample_4 = WQ_Sample.objects.create_sample(45, 'Vernier', 89,
                                                   'Manual', 9, 'Vernier',
                                                   3.25, 'Vernier', 0.879,
                                                   'Manual', 8, 'Vernier',
                                                   0, 0, 0, 0, 2.5, 0, 0, 0)

        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp_unit='Celsius',
                                              air_temp_unit='Celsius',
                                              sample_1=sample_1,
                                              sample_2=sample_2,
                                              sample_3=sample_3,
                                              sample_4=sample_4,
                                              notes='Test data made')

        # Assert that the required fields for each of the 4 samples are created
        # for the datasheet
        self.assertEqual(waterq.sample_1.water_temperature, 35)
        self.assertEqual(waterq.sample_1.water_temp_tool, 'Manual')
        self.assertEqual(waterq.sample_1.air_temperature, 70)
        self.assertEqual(waterq.sample_1.air_temp_tool, 'Manual')
        self.assertEqual(waterq.sample_1.dissolved_oxygen, 6)
        self.assertEqual(waterq.sample_1.oxygen_tool, 'Manual')
        self.assertEqual(waterq.sample_1.pH, 8.65)
        self.assertEqual(waterq.sample_1.pH_tool, 'Vernier')
        self.assertEqual(waterq.sample_1.turbidity, 0.879)
        self.assertEqual(waterq.sample_1.turbid_tool, 'Manual')
        self.assertEqual(waterq.sample_1.salinity, 8.8)
        self.assertEqual(waterq.sample_1.salt_tool, 'Vernier')

        self.assertEqual(waterq.sample_2.water_temperature, 35)
        self.assertEqual(waterq.sample_2.water_temp_tool, 'Vernier')
        self.assertEqual(waterq.sample_2.air_temperature, 70)
        self.assertEqual(waterq.sample_2.air_temp_tool, 'Vernier')
        self.assertEqual(waterq.sample_2.dissolved_oxygen, 5)
        self.assertEqual(waterq.sample_2.oxygen_tool, 'Vernier')
        self.assertEqual(waterq.sample_2.pH, 0.5)
        self.assertEqual(waterq.sample_2.pH_tool, 'Manual')
        self.assertEqual(waterq.sample_2.turbidity, 8.79)
        self.assertEqual(waterq.sample_2.turbid_tool, 'Vernier')
        self.assertEqual(waterq.sample_2.salinity, 8)
        self.assertEqual(waterq.sample_2.salt_tool, 'Manual')

        self.assertEqual(waterq.sample_3.water_temperature, 25)
        self.assertEqual(waterq.sample_3.water_temp_tool, 'Manual')
        self.assertEqual(waterq.sample_3.air_temperature, 57)
        self.assertEqual(waterq.sample_3.air_temp_tool, 'Vernier')
        self.assertEqual(waterq.sample_3.dissolved_oxygen, 12)
        self.assertEqual(waterq.sample_3.oxygen_tool, 'Manual')
        self.assertEqual(waterq.sample_3.pH, 8.45)
        self.assertEqual(waterq.sample_3.pH_tool, 'Vernier')
        self.assertEqual(waterq.sample_3.turbidity, 0.87)
        self.assertEqual(waterq.sample_3.turbid_tool, 'Manual')
        self.assertEqual(waterq.sample_3.salinity, 9.8)
        self.assertEqual(waterq.sample_3.salt_tool, 'Vernier')

        self.assertEqual(waterq.sample_4.water_temperature, 45)
        self.assertEqual(waterq.sample_4.water_temp_tool, 'Vernier')
        self.assertEqual(waterq.sample_4.air_temperature, 89)
        self.assertEqual(waterq.sample_4.air_temp_tool, 'Manual')
        self.assertEqual(waterq.sample_4.dissolved_oxygen, 9)
        self.assertEqual(waterq.sample_4.oxygen_tool, 'Vernier')
        self.assertEqual(waterq.sample_4.pH, 3.25)
        self.assertEqual(waterq.sample_4.pH_tool, 'Vernier')
        self.assertEqual(waterq.sample_4.turbidity, 0.879)
        self.assertEqual(waterq.sample_4.turbid_tool, 'Manual')
        self.assertEqual(waterq.sample_4.salinity, 8)
        self.assertEqual(waterq.sample_4.salt_tool, 'Vernier')

    def test_datasheet_AdditionalParams(self):
        """Tests that a datasheet correctly corresponds to a specified
           measurement entry - additional fields"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')

        sample_1 = WQ_Sample.objects.create_sample(35, 'Manual', 70,
                                                   'Manual', 6, 'Manual',
                                                   8.65, 'Vernier', 0.879,
                                                   'Manual', 8.8, 'Vernier',
                                                   15, 10, 7, 0.93,
                                                   2.1, 1.9, 14.5, 13)

        sample_2 = WQ_Sample.objects.create_sample(35, 'Vernier', 70,
                                                   'Vernier', 5, 'Vernier',
                                                   0.5, 'Manual', 8.79,
                                                   'Vernier', 8, 'Manual',
                                                   1, 0.10, 29, 0.93, 2.1,
                                                   2.0, 1.45, 10)

        sample_3 = WQ_Sample.objects.create_sample(25, 'Manual', 57,
                                                   'Vernier', 12, 'Manual',
                                                   8.45, 'Vernier', 0.87,
                                                   'Manual', 9.8, 'Vernier')

        sample_4 = WQ_Sample.objects.create_sample(45, 'Vernier', 89,
                                                   'Manual', 9, 'Vernier',
                                                   3.25, 'Vernier', 0.879,
                                                   'Manual', 8, 'Vernier',
                                                   0, 0, 0, 0, 2.5, 0, 0, 0)

        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp_unit='Celsius',
                                              air_temp_unit='Celsius',
                                              sample_1=sample_1,
                                              sample_2=sample_2,
                                              sample_3=sample_3,
                                              sample_4=sample_4,
                                              notes='Test data made')

        # Asserting that the additional params are properly created, if the
        # field is left blank, default to ``None``
        self.assertEqual(waterq.sample_1.conductivity, 15)
        self.assertEqual(waterq.sample_1.total_solids, 10)
        self.assertEqual(waterq.sample_1.bod, 7)
        self.assertEqual(waterq.sample_1.ammonia, 0.93)
        self.assertEqual(waterq.sample_1.nitrite, 2.1)
        self.assertEqual(waterq.sample_1.nitrate, 1.9)
        self.assertEqual(waterq.sample_1.phosphates, 14.5)
        self.assertEqual(waterq.sample_1.fecal_coliform, 13)

        self.assertEqual(waterq.sample_2.conductivity, 1)
        self.assertEqual(waterq.sample_2.total_solids, 0.10)
        self.assertEqual(waterq.sample_2.bod, 29)
        self.assertEqual(waterq.sample_2.ammonia, 0.93)
        self.assertEqual(waterq.sample_2.nitrite, 2.1)
        self.assertEqual(waterq.sample_2.nitrate, 2.0)
        self.assertEqual(waterq.sample_2.phosphates, 1.45)
        self.assertEqual(waterq.sample_2.fecal_coliform, 10)

        self.assertEqual(waterq.sample_3.conductivity, None)
        self.assertEqual(waterq.sample_3.total_solids, None)
        self.assertEqual(waterq.sample_3.bod, None)
        self.assertEqual(waterq.sample_3.ammonia, None)
        self.assertEqual(waterq.sample_3.nitrite, None)
        self.assertEqual(waterq.sample_3.nitrate, None)
        self.assertEqual(waterq.sample_3.phosphates, None)
        self.assertEqual(waterq.sample_3.fecal_coliform, None)

        self.assertEqual(waterq.sample_4.conductivity, 0)
        self.assertEqual(waterq.sample_4.total_solids, 0)
        self.assertEqual(waterq.sample_4.bod, 0)
        self.assertEqual(waterq.sample_4.ammonia, 0)
        self.assertEqual(waterq.sample_4.nitrite, 2.5)
        self.assertEqual(waterq.sample_4.nitrate, 0)
        self.assertEqual(waterq.sample_4.phosphates, 0)
        self.assertEqual(waterq.sample_4.fecal_coliform, 0)
        """
# Note: Not of high priority (since Django probably doesn't allow it in the
#       first place), but may want to eventually add tests that assert
#       datasheet creation fails when given a nonexistent or bad site
#           * def test_datasheet_nonexistent_site(self):
#           * def test_datasheet_bad_site(self):
