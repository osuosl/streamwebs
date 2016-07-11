from django.test import TestCase
from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import TransectZone

class TransectZoneTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'conifers': models.PositiveSmallIntegerField,
            'hardwoods': models.PositiveSmallIntegerField,
            'shrubs': models.PositiveSmallIntegerField,
            'comments': models.CharField,
            'id': models.AutoField,

        # Foreign key relation
            'zone_1': models.ManyToOneRel,
            'zone_2': models.ManyToOneRel,
            'zone_3': models.ManyToOneRel,
            'zone_4': models.ManyToOneRel,
            'zone_5': models.ManyToOneRel,
        }

    def test_fields_exist(self):
        for field, field_type in self.expected_fields.items():
            self.assertEqual(field_type,
                             type(TransectZone._meta.get_field(field)))

    def test_no_extra_fields(self):
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in TransectZone._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))
