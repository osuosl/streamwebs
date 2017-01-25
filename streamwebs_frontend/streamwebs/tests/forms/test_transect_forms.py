from __future__ import print_function
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

        self.optional_fields = ('comments',)

    def test_form_fields_exist(self):
        zone_form = TransectZoneForm()
        self.assertEqual(set(zone_form.Meta.fields), set(self.expected_fields))

    def test_optional_fields(self):
        zone_form = TransectZoneForm()
        for field in self.optional_fields:
            self.assertEqual(zone_form.base_fields[field].required, False)


class RiparianTransectFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'school',
            'date_time',
            'weather',
            'slope',
            'notes',
        )

        self.required_fields = (
            'school',
        )

    def test_form_fields_exist(self):
        transect_form = RiparianTransectForm()
        self.assertEqual(set(transect_form.Meta.fields),
                         set(self.expected_fields))

    def test_required_fields(self):
        transect_form = RiparianTransectForm()
        for field in self.required_fields:
            self.assertEqual(transect_form.base_fields[field].required, True)
