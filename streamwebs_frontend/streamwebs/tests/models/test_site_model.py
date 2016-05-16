from django.test import TestCase

from streamwebs.models import Site
from django.contrib.gis.db import models


class SiteTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site_name': models.TextField,
            'site_type': models.TextField,
            'description': models.TextField,
            'site_slug': models.SlugField,  # Note: max_length defaults to 50
            'location': models.PointField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'id': models.AutoField
        }

        self.optional_fields = {
            'description'
        }

    def test_fields_exist(self):
        model = models.get_model('streamwebs', 'site')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field[0])))

    def test_no_extra_fields(self):
        fields = Site._meta.get_fields()
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        models.get_model('streamwebs', 'site')
        for field in self.optional_fields:
            self.assertEqual(
                Site._meta.get_field_by_name(field)[0].blank, True)

    def test_create_and_mod_dates(self):
        """When a new site is created, both date fields should be set"""
        self.assertTrue(Site._meta.get_field('modified').auto_now)
        self.assertTrue(Site._meta.get_field('created').auto_now_add)

#    def test_modify_date(self):
#        """Test that only the 'modified' date changes when site info is
#           updated"""
#        self.assertTrue(Site._meta_.get_field('modified').auto_now)
#        self.assertEqual()

