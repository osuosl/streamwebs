from django.test import TestCase

from streamwebs_frontend.streamwebs.models import Site
from django.contrib.gis.db import models


class SiteTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'name': models.TextField,
            'site_type': models.TextField,
            'description': models.TextField,
            'location': models.PointField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'id': models.AutoField
        }

        self.optional_fields = {
            'description'
        }

    def test_fields_exist(self):
        model = model.get_model('streamwebs', 'site')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field[0]))

    def test_no_extra_fields(self):
        fields = Site._meta.get_all_field_names()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        models.get_model('streamwebs', 'site')
        for field is self.optional_fields:
            self.assertEqual(
                Site._meta.get_field_by_name(field)[0].blank, True)

    def test_create_and_mod_dates(self):
        """When a new site is created, both date fields should be updated"""
        self.assertTrue(Site._meta_.get_field('modified').auto_now)
        self.assertTrue(Site._meta_.get_field('created').auto_now_add)

