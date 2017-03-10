from django.test import TestCase
from streamwebs.forms import ResourceForm


class ResourceFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'name',
            'res_type',
            'downloadable',
            'thumbnail',
            'sort_order',
        )

        self.required_fields = (
            'name',
            'res_type',
            'sort_order',
        )

        self.optional_fields = (
            'downloadable',
            'thumbnail',
        )
        self.res_form = ResourceForm()

    def test_form_fields_exist(self):
        self.assertEqual(set(self.res_form.Meta.fields),
                         set(self.expected_fields))

    def test_required_fields(self):
        for field in self.required_fields:
            self.assertEqual(self.res_form.base_fields[field].required, True)

    def test_optional_fields(self):
        for field in self.optional_fields:
            self.assertEqual(self.res_form.base_fields[field].required, False)
