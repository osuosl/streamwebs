from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Site
from streamwebs.models import Water_Quality
from streamwebs.models import Measurements


class WaterQualityTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'DEQ_wq_level': models.CharField,
            'date': models.DateField,
            'school': models.CharField,
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'fish_present': models.BooleanField,
            'live_fish': models.PositiveSmallIntegerField,
            'dead_fish': models.PositiveSmallIntegerField,
            'water_temp_unit': models.CharField,
            'air_temp_unit': models.CharField,
            'water_temp': models.DecimalField,
            'water_temp_info': models.ForeignKey,
            'air_temp': models.DecimalField,
            'air_temp_info': models.ForeignKey,
            'dissolved_oxygen': models.DecimalField,
            'oxygen_info': models.ForeignKey,
            'pH': models.DecimalField,
            'pH_info': models.ForeignKey,
            'turbidity': models.DecimalField,
            'turbid_info': models.ForeignKey,
            'salinity': models.DecimalField,
            'salt_info': models.ForeignKey,
            'conductivity': models.DecimalField,
            'total_solids': models.DecimalField,
            'bod': models.DecimalField,
            'ammonia': models.DecimalField,
            'nitrite': models.DecimalField,
            'nitrate': models.DecimalField,
            'phosphates': models.DecimalField,
            'fecal_coliform': models.DecimalField,
            'notes': models.TextField,
            'id': models.AutoField,

            # Corresponding measurement entry (id)
            'water_temp_info_id': models.ForeignKey,
            'air_temp_info_id': models.ForeignKey,
            'oxygen_info_id': models.ForeignKey,
            'pH_info_id': models.ForeignKey,
            'turbid_info_id': models.ForeignKey,
            'salt_info_id': models.ForeignKey
        }

        self.optional_fields = {
            'conductivity',
            'total_solids',
            'bod',
            'ammonia',
            'nitrite',
            'nitrate',
            'phosphates',
            'fecal_coliform',
            'notes',
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'water_quality')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Water_Quality._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        apps.get_model('streamwebs', 'water_quality')
        for field in self.optional_fields:
            self.assertEqual(
                Water_Quality._meta.get_field(field).blank, True)

    def test_datasheet_ManyToOneSite(self):
        """Tests that a datasheet correctly corresponds to a specified site"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        water_temp_info = Measurements.objects.create_measurement_info \
                          ('Water Quality', 'Water Temperature', 1, 'Manual')
        air_temp_info = Measurements.objects.create_measurement_info \
                        ('Water Quality', 'Air Temperature', 1, 'Manual')
        oxygen_info = Measurements.objects.create_measurement_info \
                      ('Water Quality', 'Dissolved Oxygen', 1, 'Manual')
        pH_info = Measurements.objects.create_measurement_info \
                  ('Water Quality', 'pH', 1, 'Manual')
        turbid_info = Measurements.objects.create_measurement_info \
                      ('Water Quality', 'Turbidity', 1, 'Manual')
        salt_info = Measurements.objects.create_measurement_info \
                    ('Water Quality', 'Salinity', 1, 'Manual')
        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp_unit='Celsius',
                                              air_temp_unit='Celsius',
                                              water_temp=45,
                                              water_temp_info=water_temp_info, 
                                              air_temp=65,
                                              air_temp_info=air_temp_info, 
                                              dissolved_oxygen=15,
                                              oxygen_info=oxygen_info,
                                              pH=6.7,
                                              pH_info=pH_info,
                                              turbidity=0,
                                              turbid_info=turbid_info,
                                              salinity=12,
                                              salt_info=salt_info)
        self.assertEqual(waterq.site.site_name, 'test')
        self.assertEqual(waterq.site.site_type, 'some_type')
        self.assertEqual(waterq.site.site_slug, 'some_slug')

########## BREAK UP THIS TEST INTO SMALLER PARTS TO TEST **EVERYTHING**
########## I.e. datasheet_type, measuring, sample, and tool
########## For each piece of measurementd info
    def test_datasheet_SetMeasurementInfo(self):
        """Tests that a datasheet correctly corresponds to a specified
           measurement entry"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        water_temp_info = Measurements.objects.create_measurement_info \
                          ('Water Quality', 'Water Temperature', 1, 'Manual')
        air_temp_info = Measurements.objects.create_measurement_info \
                        ('Water Quality', 'Air Temperature', 1, 'Manual')
        oxygen_info = Measurements.objects.create_measurement_info \
                      ('Water Quality', 'Dissolved Oxygen', 1, 'Manual')
        pH_info = Measurements.objects.create_measurement_info \
                  ('Water Quality', 'pH', 1, 'Manual')
        turbid_info = Measurements.objects.create_measurement_info \
                      ('Water Quality', 'Turbidity', 1, 'Manual')
        salt_info = Measurements.objects.create_measurement_info \
                    ('Water Quality', 'Salinity', 1, 'Manual')
        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp_unit='Celsius',
                                              air_temp_unit='Celsius',
                                              water_temp=45,
                                              water_temp_info=water_temp_info, 
                                              air_temp=65,
                                              air_temp_info=air_temp_info, 
                                              dissolved_oxygen=15,
                                              oxygen_info=oxygen_info,
                                              pH=6.7,
                                              pH_info=pH_info,
                                              turbidity=0,
                                              turbid_info=turbid_info,
                                              salinity=12,
                                              salt_info=salt_info)
        self.assertEqual(waterq.water_temp_info.measuring, 'Water Temperature')
        self.assertEqual(waterq.air_temp_info.measuring, 'Air Temperature')
        self.assertEqual(waterq.oxygen_info.measuring, 'Dissolved Oxygen')
        self.assertEqual(waterq.pH_info.measuring, 'pH')
        self.assertEqual(waterq.turbid_info.measuring, 'Turbidity')
        self.assertEqual(waterq.salt_info.measuring, 'Salinity')

# Note: Not of high priority (since Django probably doesn't allow it in the
#       first place), but may want to eventually add tests that assert
#       datasheet creation fails when given a nonexistent or bad site
#           * def test_datasheet_nonexistent_site(self):
#           * def test_datasheet_bad_site(self):
