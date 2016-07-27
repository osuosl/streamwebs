from django.test import TestCase
from streamwebs.forms import WQForm, WQSampleForm


class WQFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'site',
            'date',
            'DEQ_wq_level',
            'latitude',
            'longitude',
            'fish_present',
            'live_fish',
            'dead_fish',
            'water_temp_unit',
            'air_temp_unit',
            'notes'
        )

    def test_WQForm_fields_exist(self):
        wq_form = WQForm()
        self.assertEqual(set(wq_form.Meta.fields),
                         set(self.expected_fields))


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

        def test_WQSampleForm_fields_exist(self):
            wq_sample_form = WQSampleForm()
            self.assertEqual(set(wq_sample_form.Meta.fields),
                             set(self.expected_fields))
