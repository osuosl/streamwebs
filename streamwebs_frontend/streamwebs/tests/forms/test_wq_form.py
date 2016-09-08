from django.test import TestCase
from streamwebs.forms import WQForm, WQSampleForm
from streamwebs.models import Site


class WQFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'site',
            'date',
            'DEQ_dq_level',
            'school',
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

    def test_WQForm_isValid(self):
        site = Site.test_objects.create_site('Site Name')
        good_data = {
            'DEQ_dq_level': u'A',
            'air_temp_unit': u'Fahrenheit',
            'water_temp_unit': u'Fahrenheit',
            'date': u'2016-08-22',
            'dead_fish': 2,
            'fish_present': u'True',
            'initial-date': u'2016-08-22',
            'latitude': 50,
            'live_fish': 5,
            'longitude': 120,
            'notes': u"Call your mom on Mother's Day!",
            'school': u'Somewhere Cool',
            'site': site.id
        }
        form = WQForm(data=good_data)
        self.assertTrue(form.is_valid())


class WQSampleFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'water_temperature',
            'water_temp_tool',
            'air_temperature',
            'air_temp_tool',
            'dissolved_oxygen',
            'oxygen_tool',
            'pH',
            'pH_tool',
            'turbidity',
            'turbid_tool',
            'salinity',
            'salt_tool',
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
            'fecal_coliform'
        }

    def test_WQSampleForm_fields_exist(self):
        wq_sample_form = WQSampleForm()
        self.assertEqual(
            set(wq_sample_form.Meta.fields), set(self.expected_fields)
        )

    def test_optional_fields(self):
        wq_sample_form = WQSampleForm()
        for field in self.optional_fields:
            self.assertEqual(
                wq_sample_form.base_fields[field].required, False
            )

    def test_Water_QualityForm_isValid(self):
        good_data = {
                'air_temp_tool': u'Manual',
                'air_temperature': u'2',
                'ammonia': u'0',
                'bod': u'0',
                'conductivity': u'1',
                'dissolved_oxygen': u'1',
                'fecal_coliform': u'0',
                'nitrate': u'0',
                'nitrite': u'0',
                'oxygen_tool': u'Manual',
                'pH': u'0',
                'pH_tool': u'Manual',
                'phosphates': u'2',
                'salinity': u'0',
                'salt_tool': u'Vernier',
                'total_solids': u'0',
                'turbid_tool': u'Manual',
                'turbidity': u'0',
                'water_temp_tool': u'Manual',
                'water_temperature': u'1',
        }
        form = WQSampleForm(data=good_data)
        self.assertTrue(form.is_valid())
