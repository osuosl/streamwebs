from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Site
from streamwebs.models import Soil_Survey


class SoilSurveyTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'school': models.ForeignKey,
            'teacher': models.CharField,
            'date': models.DateTimeField,
            'weather': models.CharField,
            'site': models.ForeignKey,
            'site_id': models.ForeignKey,

            'landscape_pos': models.CharField,
            'cover_type': models.CharField,
            'land_use': models.CharField,

            'distance': models.CharField,
            'site_char': models.TextField,
            'soil_type': models.CharField,

            'id': models.AutoField,
        }

        self.optional_fields = {
            'site_char'
        }

        self.site = Site.test_objects.create_site('test site',
                                                  'test site type',
                                                  'test_site_slug')

    def test_fields_exist(self):
        """Tests that all fields are successfully created"""
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(Soil_Survey._meta.get_field(field)))

    def test_no_extra_fields(self):
        """Tests that there are no extra fields"""
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Soil_Survey._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))

        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        """Tests that optional fields default to True when left blank"""
        apps.get_model('streamwebs', 'soil_survey')
        for field in self.optional_fields:
            self.assertEqual(
                Soil_Survey._meta.get_field(field).blank, True)
