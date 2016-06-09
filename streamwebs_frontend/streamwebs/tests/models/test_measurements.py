from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Measurements


class MeasurementsTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'datasheet_type': models.CharField,
            'sample_number': models.CharField,
            'air_temp_unit': models.CharField,
            'water_temp_unit': models.CharField,
            'tool': models.CharField,
            'id': models.AutoField,

            # Datasheets
            'water_quality': models.ManyToOneRel
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'measurements')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra_fields(self):
        fields = list(set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Measurements._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))
