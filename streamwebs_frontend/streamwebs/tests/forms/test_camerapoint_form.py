from django.test import TestCase
from streamwebs.forms import CameraPointForm


class CameraPointFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'site',
            'cp_date',
            'location',
            'map_datum',
            'description'
        )

        self.required_fields = (
            'site',
            'cp_date',
            'location',
        )

        self.camera_pt_form = CameraPointForm()

    def test_form_fields_exist(self):
        self.assertEqual(set(self.camera_pt_form.Meta.fields),
                         set(self.expected_fields))

    def test_required_fields(self):
        for field in self.required_fields:
            self.assertEqual(self.camera_pt_form.base_fields[field].required,
                             True)
