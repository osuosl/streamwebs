from django.test import TestCase

from streamwebs.models import Water_Quality
from django.contrib.gis.db import models
from django.apps import apps
from itertools import chain

class WaterQualityTestCase(TestCase):

    def setUp(self):
        self.expected_fields = {
            'site_name': models.ForeignKey,
            'date': models.DateField,
            'time': models.TimeField, 
            'school': models.CharField,
            'teacher': models.CharField,
            'latitude': models.DecimalField,
            'longitude': models.DecimalField,
            'fish_present': models.BooleanField,
            'live_fish': models.PositiveSmallIntegerField,
            'dead_fish': models.PositiveSmallIntegerField,
            'water_temp': models.DecimalField,
            'air_temp': models.DecimalField,
            'dissolved_O2': models.DecimalField,
            'pH': models.DecimalField,
            'turbidity': models.DecimalField,
            'id': models.AutoField
        }

        # Where does 'Vernier' and 'Manual' fit into the model?
        # Celcius and Fahrenheit?
        # Sample number??

        self.optional_fields = {
            'live_fish',
            'dead_fish'
        }

    def test_fields_exist(self):
        model = apps.get_model('streamwebs', 'water_quality')
        for field, field_type in self.expected_field.items():
            self.asserEqual(
                field_type, type(model._meta.get_field(field)))

    def test_no_extra fields(self):
        fields = list(set(chain.from_iterable(
            (field_name, field.attname) if hasattr(field, 'attname') else
            (field.name,) for field in Water_Quality._meta.get_fields()
            if not (field.many_to_one and field.related_model is None)
        )))
        self.assertEqual(sorted(fields), sorted(self.expected_fields.keys()))

    def test_optional_fields(self):
        apps.get_model('streamwebs', 'site')
        for field in self.optional_fields:
            self.assertEqual(
                Water_Quality._meta.get_field(field).blank, True)

    def test_datasheet_OneToOne(self):
        site = Site.objects.create_site('name', 'type', 'slug');
        waterq = 
