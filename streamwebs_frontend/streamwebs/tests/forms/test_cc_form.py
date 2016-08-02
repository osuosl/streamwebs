from django.test import TestCase
from streamwebs.forms import Canopy_Cover_Form, CC_Cardinal_Form


class Canopy_Cover_Form_TestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'school',
            'date_time',
            'site',
            'weather',
            'north',
            'east',
            'south',
            'west',
            'est_canopy_cover'
        )

    def test_Canopy_Cover_Form_fields_exist(self):
        cc_form = Canopy_Cover_Form()
        self.assertEqual(set(cc_form.Meta.fields),
                         set(self.expected_fields))

    def test_Canopy_Cover_Form_required_fields(self):
        cc_form = Canopy_Cover_Form()
        for field in self.expected_fields:
            self.assertEqual(cc_form.base_fields[field].required, True)


class CC_Cardinal_Form_TestCase(TestCase):

    def setUp(self):
        self.expected_fields = ('direction', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                                'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'num_shaded')

    def test_CC_Cardinal_Form_fields_exist(self):
        cc_cardinal_form = CC_Cardinal_Form()
        self.assertEqual(set(cc_cardinal_form.Meta.fields),
                         set(self.expected_fields))

    def test_CC_Cardinal_Form_required_fields(self):
        cardinal_form = CC_Cardinal_Form()
        self.assertEqual(cardinal_form.base_fields['direction'].required,
                         True)
        self.assertEqual(cardinal_form.base_fields['num_shaded'].required,
                         True)

    def test_CC_Cardinal_Form_optional_fields(self):
        cardinal_form = CC_Cardinal_Form()
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWX':
            self.assertEqual(cardinal_form.base_fields[letter].required, False)
