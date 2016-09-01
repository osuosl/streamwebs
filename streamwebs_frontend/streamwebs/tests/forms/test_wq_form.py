from django.test import TestCase
from streamwebs.forms import WQForm, WQSampleForm


class WQFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'site',
            'date',
            'DEQ_dq_level',
            'latitude',
            'longitude',
            'fish_present',
            'live_fish',
            'dead_fish',
            'water_temp_unit',
            'air_temp_unit',
            'notes'
        )

        self.optional_fields = {
            'notes'
        }

    def test_WQForm_fields_exist(self):
        wq_form = WQForm()
        self.assertEqual(set(wq_form.Meta.fields),
                         set(self.expected_fields))

    def test_optional_fields(self):
        wq_form = WQForm()
        for field in self.optional_fields:
            self.assertEqual(
                wq_form.base_fields[field].required, False)


class WQSampleFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'water_temperature',
            'air_temperature',
            'dissolved_oxygen',
            'pH',
            'turbidity',
            'salinity',
            'conductivity',
            'total_solids',
            'bod',
            'ammonia',
            'nitrite',
            'nitrate',
            'phosphates',
            'fecal_coliform'
        )

        self.optional_fields = {
            'conductivity',
            'total_solids',
            'bod',
            'ammonia',
            'nitrite',
            'nitrate',
            'phosphates',
        }

    def test_WQSampleForm_fields_exist(self):
        wq_sample_form = WQSampleForm()
        self.assertEqual(set(wq_sample_form.Meta.fields),
                         set(self.expected_fields))

    def test_optional_fields(self):
        wq_sample_form = WQSampleForm()
        for field in self.optional_fields:
            self.assertEqual(
                wq_sample_form.base_fields[field].required, False)
