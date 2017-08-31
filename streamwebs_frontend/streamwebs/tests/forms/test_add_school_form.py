from django.test import TestCase
from streamwebs.forms import SchoolForm


class SchoolFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'school_type',
            'name',
            'address',
            'city',
            'province',
            'zipcode'
        )
        self.required_fields = (
            'school_type',
            'name',
            'address',
            'city',
            'province',
            'zipcode'
        )

        self.school_form = SchoolForm()

        def test_form_fields_exist(self):
            self.assertEqual(set(self.school_form.Meta.fields),
                             set(self.expected_fields))

        def test_required_fields(self):
            for field in self.required_fields:
                self.assertEqual(self.school_form.base_fields[field].required,
                                 True)
