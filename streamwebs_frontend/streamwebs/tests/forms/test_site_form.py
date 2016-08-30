from django.test import TestCase
from streamwebs.forms import SiteForm


class SiteFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'site_name',
            'description',
            'location',
            'image'
        )

        self.required_fields = (
            'site_name',
            'location'
        )

        self.optional_fields = (
            'description',
            'image'
        )

    def test_SiteForm_fields_exist(self):
        site_form = SiteForm()
        self.assertEqual(set(site_form.Meta.fields), set(self.expected_fields))

    def test_SiteForm_required_fields(self):
        site_form = SiteForm()
        for field in self.required_fields:
            self.assertEqual(site_form.base_fields[field].required, True)

    def test_SiteForm_optional_fields(self):
        site_form = SiteForm()
        for field in self.optional_fields:
            self.assertEqual(site_form.base_fields[field].required, False)
