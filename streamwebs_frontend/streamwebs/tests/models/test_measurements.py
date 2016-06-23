from django.test import TestCase

from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

from streamwebs.models import Measurements


class MeasurementsTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'datasheet_type': models.CharField,
            'measuring': models.CharField,
            'sample_number': models.CharField,
            'tool': models.CharField,
            'id': models.AutoField,

            # Datasheet relations
            'water_temp_info': models.ManyToOneRel,
            'air_temp_info': models.ManyToOneRel,
            'oxygen_info': models.ManyToOneRel,
            'pH_info': models.ManyToOneRel,
            'turbid_info': models.ManyToOneRel,
            'salt_info': models.ManyToOneRel,
            'conductivity_info': models.ManyToOneRel,
            'bod_info': models.ManyToOneRel,
            'tot_solids_info': models.ManyToOneRel,
            'ammonia_info': models.ManyToOneRel,
            'nitrite_info': models.ManyToOneRel,
            'nitrate_info': models.ManyToOneRel,
            'phosphate_info': models.ManyToOneRel,
            'fecal_info': models.ManyToOneRel
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
