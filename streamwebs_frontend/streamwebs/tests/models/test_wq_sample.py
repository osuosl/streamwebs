from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain
from django.core.exceptions import ValidationError
from streamwebs.models import Water_Quality, WQ_Sample, Site
from streamwebs.models import validate_pH


class WQSampleTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'water_temperature': models.DecimalField,
            'water_temp_tool': models.CharField,
            'air_temperature': models.DecimalField,
            'air_temp_tool': models.CharField,
            'dissolved_oxygen': models.DecimalField,
            'oxygen_tool': models.CharField,
            'pH': models.DecimalField,
            'pH_tool': models.CharField,
            'turbidity': models.DecimalField,
            'turbid_tool': models.CharField,
            'salinity': models.DecimalField,
            'salt_tool': models.CharField,
            'conductivity': models.DecimalField,
            'total_solids': models.DecimalField,
            'bod': models.DecimalField,
            'ammonia': models.DecimalField,
            'nitrite': models.DecimalField,
            'nitrate': models.DecimalField,
            'phosphates': models.DecimalField,
            'fecal_coliform': models.DecimalField,
            'id': models.AutoField,

            # List the foreign key relation here
            'water_quality': models.ForeignKey,
            'water_quality_id': models.ForeignKey,
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
        }

        site = Site.test_objects.create_site('test site', 'test site type',
                                             'test_site_slug')

        self.water_quality = Water_Quality.objects.create_water_quality(
                             site, '2016-08-03', 'a', 'A', 90, 123,
                             False, 0, 0, 'Fahrenheit', 'Fahrenheit')

        # Object to test pH
        self.sample_data = WQ_Sample.objects.create_sample(
            self.water_quality, 35, 'Manual', 70,
            'Manual', 6, 'Manual',
            16, 'Vernier', 0.879,
            'Manual', 8.8, 'Vernier',
            15, 10, 7, 0.93,
            2.1, 1.9, 14.5, 13
        )

    def test_fields_exist(self):
        """Tests that model fields are successfully created"""
        model = apps.get_model('streamwebs', 'wq_sample')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        """Checks for discrepancies between the actual model and is expected
           fields"""
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in WQ_Sample._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        """Tests that optional fields default to true when left blank"""
        sample = apps.get_model('streamwebs', 'wq_sample')
        for field in self.optional_fields:
            self.assertEqual(
                sample._meta.get_field(field).blank, True)

    def test_Sample_ManyToOneWaterQuality(self):
        sample_1 = WQ_Sample.objects.create_sample(self.water_quality, 34,
                                                   'Vernier',
                                                   55, 'Manual',
                                                   4.2, 'Vernier',
                                                   9, 'Manual',
                                                   0.44, 'Manual',
                                                   5.6, 'Vernier')
        sample_2 = WQ_Sample.objects.create_sample(self.water_quality, 23,
                                                   'Vernier',
                                                   65, 'Manual',
                                                   2.5, 'Vernier',
                                                   9, 'Manual',
                                                   0.41, 'Manual',
                                                   7.6, 'Vernier')

        self.assertEqual(sample_1.water_quality.school, 'a')
        self.assertEqual(sample_1.water_quality.date, '2016-08-03')
        self.assertEqual(sample_1.water_quality.site.site_name, 'test site')

        self.assertEqual(sample_2.water_quality.school, 'a')
        self.assertEqual(sample_2.water_quality.date, '2016-08-03')
        self.assertEqual(sample_2.water_quality.site.site_name, 'test site')

    def test_sample_creation_req_fields(self):
        sample = WQ_Sample.objects.create_sample(self.water_quality, 23,
                                                 'Vernier',
                                                 65, 'Manual',
                                                 2.5, 'Vernier',
                                                 9, 'Manual',
                                                 0.41, 'Manual',
                                                 7.6, 'Vernier')

        # Required
        self.assertEqual(sample.water_quality.site.site_name, 'test site')
        self.assertEqual(sample.water_temperature, 23)
        self.assertEqual(sample.water_temp_tool, 'Vernier')
        self.assertEqual(sample.air_temperature, 65)
        self.assertEqual(sample.air_temp_tool, 'Manual')
        self.assertEqual(sample.dissolved_oxygen, 2.5)
        self.assertEqual(sample.oxygen_tool, 'Vernier')
        self.assertEqual(sample.pH, 9)
        self.assertEqual(sample.pH_tool, 'Manual')
        self.assertEqual(sample.turbidity, 0.41)
        self.assertEqual(sample.turbid_tool, 'Manual')
        self.assertEqual(sample.salinity, 7.6)
        self.assertEqual(sample.salt_tool, 'Vernier')

        # Optional
        self.assertEqual(sample.conductivity, None)
        self.assertEqual(sample.total_solids, None)
        self.assertEqual(sample.bod, None)
        self.assertEqual(sample.ammonia, None)
        self.assertEqual(sample.nitrite, None)
        self.assertEqual(sample.nitrate, None)
        self.assertEqual(sample.phosphates, None)
        self.assertEqual(sample.fecal_coliform, None)

    def test_sample_creation_opt_fields(self):
        sample = WQ_Sample.objects.create_sample(self.water_quality, 0, 0,
                                                 0, 0, 0, 0, 0, 0, 0, 0,
                                                 0, 0, 35, 2, 0.34, 3.23,
                                                 12, 37, 0.34, 1.45)

        # Required
        self.assertEqual(sample.water_quality.site.site_name, 'test site')
        self.assertEqual(sample.water_temperature, 0)
        self.assertEqual(sample.water_temp_tool, 0)
        self.assertEqual(sample.air_temperature, 0)
        self.assertEqual(sample.air_temp_tool, 0)
        self.assertEqual(sample.dissolved_oxygen, 0)
        self.assertEqual(sample.oxygen_tool, 0)
        self.assertEqual(sample.pH, 0)
        self.assertEqual(sample.pH_tool, 0)
        self.assertEqual(sample.turbidity, 0)
        self.assertEqual(sample.turbid_tool, 0)
        self.assertEqual(sample.salinity, 0)
        self.assertEqual(sample.salt_tool, 0)

        # Optional
        self.assertEqual(sample.conductivity, 35)
        self.assertEqual(sample.total_solids, 2)
        self.assertEqual(sample.bod, 0.34)
        self.assertEqual(sample.ammonia, 3.23)
        self.assertEqual(sample.nitrite, 12)
        self.assertEqual(sample.nitrate, 37)
        self.assertEqual(sample.phosphates, 0.34)
        self.assertEqual(sample.fecal_coliform, 1.45)

    # Tests for pH validator. Valid pH's are 0-14.
    def test_validate_pH_too_large(self):
        with self.assertRaises(ValidationError):
            validate_pH(self.sample_data.pH)

    def test_validate_pH_too_small(self):
        self.sample_data.pH = -1
        self.sample_data.save()
        with self.assertRaises(ValidationError):
            validate_pH(self.sample_data.pH)

    def test_validate_pH_good(self):
        self.sample_data.pH = 7
        self.sample_data.save()
        self.assertEqual(validate_pH(self.sample_data.pH), None)
