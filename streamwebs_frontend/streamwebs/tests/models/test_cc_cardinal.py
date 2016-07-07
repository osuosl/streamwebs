from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import CC_Cardinal


class CCCardinalTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'A': models.BooleanField,
            'B': models.BooleanField,
            'C': models.BooleanField,
            'D': models.BooleanField,
            'E': models.BooleanField,
            'F': models.BooleanField,
            'G': models.BooleanField,
            'H': models.BooleanField,
            'I': models.BooleanField,
            'J': models.BooleanField,
            'K': models.BooleanField,
            'L': models.BooleanField,
            'M': models.BooleanField,
            'N': models.BooleanField,
            'O': models.BooleanField,
            'P': models.BooleanField,
            'Q': models.BooleanField,
            'R': models.BooleanField,
            'S': models.BooleanField,
            'T': models.BooleanField,
            'U': models.BooleanField,
            'V': models.BooleanField,
            'W': models.BooleanField,
            'X': models.BooleanField,
            'shaded': models.PositiveIntegerField,

           # # Foreign key relations
           # 'north': ManyToOneRel,
           # 'east': ManyToOneRel,
           # 'south': ManyToOneRel,
           # 'west': ManyToOneRel
        }

    def test_fields_exist(self):
        """Check that all expected fields have been created"""
        model = apps.get_model('streamwebs', 'cc_cardinal')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        """Check that there are no inconsistencies between the (actual) model
           and its expected fields"""
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in CC_Cardinal._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))
