from django.test import TestCase
from streamwebs.forms import SoilSurveyForm


class SoilSurveyFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'school',
            'date',
            'weather',
            'landscape_pos',
            'cover_type',
            'land_use',
            'distance',
            'site_char',
            'soil_type'
        )

        self.optional_fields = ('site_char',)

    def test_form_fields_exist(self):
        soil_form = SoilSurveyForm()
        self.assertEqual(set(soil_form.Meta.fields), set(self.expected_fields))

    def test_optional_fields(self):
        soil_form = SoilSurveyForm()
        for field in self.optional_fields:
            self.assertEqual(soil_form.base_fields[field].required, False)
