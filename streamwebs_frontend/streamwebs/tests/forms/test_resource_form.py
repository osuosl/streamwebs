from django.test import TestCase
from streamwebs.forms import Resource_Data_Sheet_Form


class Data_Sheet_TestCase(TestCase):

    def setUp(self):
        self.expected_fields = (
            # 'id',
            # 'sort_order'
            'name',
            'res_type',
            'downloadable',
            'thumbnail'
        )

        self.optional_fields = ('downloadable', 'thumbnail')

    def test_DSForm_fields_exist(self):
        ds_form = Resource_Data_Sheet_Form()
        self.assertEqual(set(ds_form.Meta.fields), set(self.expected_fields))

    def test_optional_fields(self):
        ds_form = Resource_Data_Sheet_Form()
        for field in self.optional_fields:
            self.assertEqual(ds_form.base_fields[field].required, False)
