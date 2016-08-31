from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Resource


class ResourceTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'id': models.AutoField,
            'name': models.CharField,
            'res_type': models.CharField,
            'downloadable': models.FileField,
            'thumbnail': models.ImageField,
            'sort_order': models.PositiveSmallIntegerField,
        }
        self.optional_fields = {
           'downloadable', 'thumbnail'
        }

    def test_fields_exist(self):
        # for field, field_type in self.expected_fields.items():
        #     self.assertEqual(
        #         field_type, type(Resource._meta.get_field(field))
        #     )
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(Resource._meta.get_field(field))
            )

    def test_no_extra_fields(self):
        # the following is equivalent to MyField._meta.get_all_field_names()
        # which was deprecated in Django 1.9
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Resource._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        apps.get_model('streamwebs', 'resource')
        for field in self.optional_fields:
            self.assertEqual(
                Resource._meta.get_field(field).blank, True
            )
