from django.test import TestCase
from streamwebs.forms import StatisticsForm


class StatisticsFormTestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            'start',
            'end'
        )
        self.stats_form = StatisticsForm();

    def test_form_fields_exist(self):
        self.assertEqual(set(self.stats_form.fields),
                         set(self.expected_fields))

    def test_optional_fields(self):
        """Both date fields should be optional."""
        for field in self.expected_fields:
            self.assertEqual(self.stats_form.base_fields[field].required,
                             False)
