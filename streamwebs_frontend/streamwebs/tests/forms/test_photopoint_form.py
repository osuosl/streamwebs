from django.test import TestCase
from streamwebs.forms import PhotoPointForm


class PhotoPointFormTestCase(TestCase):
    def setUp(self):
        self.expected_fields = (
            'compass_bearing',
            'distance',
            'camera_height',
            'notes'
        )

        self.required_fields = (
            'compass_bearing',
        )

        self.optional_fields = (
            'notes',
            'distance',
            'camera_height',
        )

        self.pp_form = PhotoPointForm()

    def test_form_fields_exist(self):
        self.assertEqual(set(self.pp_form.Meta.fields),
                         set(self.expected_fields))

    def test_required_fields(self):
        for field in self.required_fields:
            self.assertEqual(self.pp_form.base_fields[field].required, True)
