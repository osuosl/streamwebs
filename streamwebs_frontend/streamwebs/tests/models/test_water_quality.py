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
            'water_temp': models.DecimalField,
            'air_temp': models.DecimalField,
            'dissolved_oxygen': models.DecimalField,
            'pH': models.DecimalField,
            'turbidity': models.DecimalField,
            'salinity': models.DecimalField,
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

            # Corresponding measurement entry
            'measurements': models.ForeignKey,
            'measurements_id': models.ForeignKey

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
        measurements = Measurements.objects.create_measures('Water Quality',
                                                             1,
                                                             'Celsius',
                                                             'Celsius',
                                                             'Manual')
        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp=45, air_temp=65,
                                              dissolved_oxygen=15, pH=6.7,
                                              turbidity=0, salinity=12,
                                              measurements=measurements)
        self.assertEqual(waterq.site.site_name, 'test')
        self.assertEqual(waterq.site.site_type, 'some_type')
        self.assertEqual(waterq.site.site_slug, 'some_slug')

    def test_datasheet_ManyToOneMeasurement(self):
        """Tests that a datasheet correctly corresponds to a specified
           measurement entry"""
        site = Site.objects.create_site('test', 'some_type', 'some_slug')
        measurements = Measurements.objects.create_measures('Water Quality',
                                                             1,
                                                             'Celsius',
                                                             'Celsius',
                                                             'Manual')
        waterq = Water_Quality.objects.create(site=site,
                                              DEQ_wq_level='A',
                                              date='2016-06-01',
                                              school='a', latitude=90,
                                              longitude=123,
                                              fish_present='False',
                                              live_fish=0, dead_fish=0,
                                              water_temp=45, air_temp=65,
                                              dissolved_oxygen=15, pH=6.7,
                                              turbidity=0, salinity=12,
                                              measurements=measurements)
        self.assertEqual(waterq.measurements.datasheet_type, 'Water Quality')
        self.assertEqual(waterq.measurements.sample_number, 1)
        self.assertEqual(waterq.measurements.air_temp_unit, 'Celsius')
        self.assertEqual(waterq.measurements.water_temp_unit, 'Celsius')
        self.assertEqual(waterq.measurements.tool, 'Manual')

# Note: Not of high priority (since Django probably doesn't allow it in the
#       first place), but may want to eventually add tests that assert
#       datasheet creation fails when given a nonexistent or bad site
#           * def test_datasheet_nonexistent_site(self):
#           * def test_datasheet_bad_site(self):
