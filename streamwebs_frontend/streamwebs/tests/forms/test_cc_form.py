from django.test import TestCase
from streamwebs.forms import Canopy_Cover_Form


class Canopy_Cover_Form_TestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'school',
            'date_time',
            'weather',
            'est_canopy_cover',
            'north_cc',
            'east_cc',
            'south_cc',
            'west_cc'
        )
        self.required_fields = (
            'school',
            'date_time',
            'est_canopy_cover',
            'north_cc',
            'east_cc',
            'south_cc',
            'west_cc'
        )

    def test_Canopy_Cover_Form_fields_exist(self):
        """Tests that fields for Canopy Cover form exist."""
        cc_form = Canopy_Cover_Form()
        self.assertEqual(set(cc_form.Meta.fields),
                         set(self.expected_fields))

    def test_Canopy_Cover_Form_required_fields(self):
        """Tests that required fields in Canopy Cover form are required."""
        cc_form = Canopy_Cover_Form()
        for field in self.required_fields:
            self.assertEqual(cc_form.base_fields[field].required, True)
