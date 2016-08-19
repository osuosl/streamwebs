from django.test import TestCase

from streamwebs.models import Site
from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain


class SiteTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site_name': models.CharField,
            'site_type': models.CharField,
            'description': models.TextField,
            'site_slug': models.SlugField,  # Note: max_length defaults to 50
            'location': models.PointField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            'id': models.AutoField,

            # Datasheets
            'water_quality': models.ManyToOneRel,
            'macroinvertebrates': models.ManyToOneRel,
            'ripariantransect': models.ManyToOneRel,
            'canopy_cover': models.ManyToOneRel
        }

        self.optional_fields = {
            'description'
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'site')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        # the following is equivalent to MyField._meta.get_all_field_names()
        # which was deprecated in Django 1.9
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Site._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        apps.get_model('streamwebs', 'site')
        for field in self.optional_fields:
            self.assertEqual(
                Site._meta.get_field(field).blank, True)
