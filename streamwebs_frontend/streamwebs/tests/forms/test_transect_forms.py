from django.test import TestCase
from streamwebs.forms import TransectZoneForm, RiparianTransectForm


class TransectZoneFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'conifers',
            'hardwoods',
            'shrubs',
            'comments'
        )

    def test_TransectZoneForm_fields_exist(self):
        zone_form = TransectZoneForm()
        self.assertEqual(set(zone_form.Meta.fields), set(self.expected_fields))


class RiparianTransectFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'school',
            'date_time',
            'weather',
            'site',
            'slope',
            'notes',
        )

    def test_RiparianTransectFormTestCase(self):
        transect_form = RiparianTransectForm()
        self.assertEqual(set(transect_form.Meta.fields),
                         set(self.expected_fields))
