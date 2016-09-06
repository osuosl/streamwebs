from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Site
from streamwebs.models import Water_Quality


class WaterQualityTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,
            'DEQ_dq_level': models.CharField,
            'date': models.DateField,
            'school': models.CharField,
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'fish_present': models.CharField,
            'live_fish': models.PositiveSmallIntegerField,
            'dead_fish': models.PositiveSmallIntegerField,
            'water_temp_unit': models.CharField,
            'air_temp_unit': models.CharField,
            'notes': models.TextField,
            'id': models.AutoField,
            'water_quality': models.ManyToOneRel,
        }

        self.optional_fields = {
            'notes'
        }

        self.site = Site.test_objects.create_site('test site', 'test type')

    def test_fields_exist(self):
        """Tests that all fields are successfully created"""
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(Water_Quality._meta.get_field(field))
            )

    def test_no_extra_fields(self):
        """Checks that there are no differences between the actual model and
           its expected fields"""
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Water_Quality._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        """Tests that optional fields default to True when left blank"""
        apps.get_model('streamwebs', 'water_quality')
        for field in self.optional_fields:
            self.assertEqual(
                Water_Quality._meta.get_field(field).blank, True
            )

    def test_datasheet_ManyToOneSite(self):
        """Tests that a datasheet correctly corresponds to a specified site"""
        site = Site.test_objects.create_site('test', 'some_type')

        waterq = Water_Quality.test_objects.create(
            site=site, DEQ_dq_level='A', date='2016-08-03',
            school='a', latitude=90, longitude=123, fish_present='False',
            live_fish=0, dead_fish=0, water_temp_unit='Fahrenheit',
            air_temp_unit='Fahrenheit', notes='Test data made')

        # Assert that site data matches the newly created test site
        self.assertEqual(waterq.site.site_name, 'test')
        self.assertEqual(waterq.site.site_type, 'some_type')
        self.assertEqual(waterq.site.site_slug, site.site_slug)

    def test_wq_creation_req_fields(self):
        wq = Water_Quality.test_objects.create_water_quality(
            self.site, '2016-08-04', 'a', 'A', 90, 123, True, 4, 5,
            'Fahrenheit', 'Fahrenheit'
        )
        # required
        self.assertEqual(wq.site.site_name, 'test site')
        self.assertEqual(wq.date, '2016-08-04')
        self.assertEqual(wq.school, 'a')
        self.assertEqual(wq.DEQ_dq_level, 'A')
        self.assertEqual(wq.latitude, 90)
        self.assertEqual(wq.longitude, 123)
        self.assertEqual(wq.fish_present, True)
        self.assertEqual(wq.live_fish, 4)
        self.assertEqual(wq.dead_fish, 5)
        self.assertEqual(wq.air_temp_unit, 'Fahrenheit')
        self.assertEqual(wq.water_temp_unit, 'Fahrenheit')

        # optional
        self.assertEqual(wq.notes, '')

    def test_wq_creation_opt_fields(self):
        wq = Water_Quality.test_objects.create_water_quality(
            self.site, '2016-08-04', 'a', 'A', 90, 123, True, 4, 5,
            'Fahrenheit', 'Fahrenheit', 'Notes on wq'
        )
        # required
        self.assertEqual(wq.site.site_name, 'test site')
        self.assertEqual(wq.date, '2016-08-04')
        self.assertEqual(wq.school, 'a')
        self.assertEqual(wq.DEQ_dq_level, 'A')
        self.assertEqual(wq.latitude, 90)
        self.assertEqual(wq.longitude, 123)
        self.assertEqual(wq.fish_present, True)
        self.assertEqual(wq.live_fish, 4)
        self.assertEqual(wq.dead_fish, 5)
        self.assertEqual(wq.air_temp_unit, 'Fahrenheit')
        self.assertEqual(wq.water_temp_unit, 'Fahrenheit')

        # optional
        self.assertEqual(wq.notes, 'Notes on wq')

    def test_longitude_range(self):
        """Tests that latitude and longitude are within correct ranges"""
        # Test that longitude will throw a ValidationError
        longHigh = Water_Quality.test_objects.create_water_quality(
            self.site, '2016-08-04', 'a', 'A', 90, 923, True, 4, 5,
            'Fahrenheit', 'Fahrenheit', 'Notes on wq'
        )
        self.assertRaises(ValidationError, longHigh.clean_fields)
        longLow = Water_Quality.test_objects.create_water_quality(
            self.site, '2016-08-04', 'a', 'A', 90, -183, True, 4, 5,
            'Fahrenheit', 'Fahrenheit', 'Notes on wq'
        )
        self.assertRaises(ValidationError, longLow.clean_fields)

    def test_latitude_range(self):
        # Test that latitude will throw a ValidationError
        latHigh = Water_Quality.test_objects.create_water_quality(
            self.site, '2016-08-04', 'a', 'A', 90, 923, True, 4, 5,
            'Fahrenheit', 'Fahrenheit', 'Notes on wq'
        )
        self.assertRaises(ValidationError, latHigh.clean_fields)
        latLow = Water_Quality.test_objects.create_water_quality(
            self.site, '2016-08-04', 'a', 'A', 90, -183, True, 4, 5,
            'Fahrenheit', 'Fahrenheit', 'Notes on wq'
        )
        self.assertRaises(ValidationError, latLow.clean_fields)

# Note: Not of high priority (since Django probably doesn't allow it in the
#       first place), but may want to eventually add tests that assert
#       datasheet creation fails when given a nonexistent or bad site
#           * def test_datasheet_nonexistent_site(self):
#           * def test_datasheet_bad_site(self):
