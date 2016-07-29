from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from django.core.exceptions import ValidationError
from itertools import chain

from streamwebs.models import CC_Cardinal, validate_shaded


class CCCardinalTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'direction': models.CharField,
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
            'num_shaded': models.PositiveIntegerField,
            'id': models.AutoField,

            # Foreign key relations
            'north': models.ManyToOneRel,
            'east': models.ManyToOneRel,
            'south': models.ManyToOneRel,
            'west': models.ManyToOneRel
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

    def test_validate_shaded_good(self):
        """Check that num_shaded is in between 0-24"""
        north = CC_Cardinal.objects.create_shade('North', True, True, False,
                                                 False, False, True, False,
                                                 False, True, True, True,
                                                 False, True, False, False,
                                                 False, True, False, True,
                                                 True, False, True, False,
                                                 False, 11)

        self.assertEqual(validate_shaded(north.num_shaded), None)

    def test_validate_shaded_too_large(self):
        """Check that validation error is risen when num_shaded
           is too large"""
        north = CC_Cardinal.objects.create_shade('North', True, True, False,
                                                 False, False, True, False,
                                                 False, True, True, True,
                                                 False, True, False, False,
                                                 False, True, False, True,
                                                 True, False, True, False,
                                                 False, 45)

        with self.assertRaises(ValidationError):
            validate_shaded(north.num_shaded)

    def test_clean_with_error(self):
        north = CC_Cardinal.objects.create_shade('North', True, True, False,
                                                 False, False, True, False,
                                                 False, True, True, True,
                                                 False, True, False, False,
                                                 False, True, False, True,
                                                 True, False, True, False,
                                                 False, 21)

        with self.assertRaises(ValidationError):
            north.clean()

    def test_clean_no_error(self):
        north = CC_Cardinal.objects.create_shade('North', True, True, False,
                                                 False, False, True, False,
                                                 False, True, True, True,
                                                 False, True, False, False,
                                                 False, True, False, True,
                                                 True, False, True, False,
                                                 False, 11)

        raised = False
        try:
            north.clean()
        except:
            raised = True
        self.assertFalse(raised, 'ValidationError raised')
