from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class CreateSchoolTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(username='john', password='johnpassword')

    def test_view_with_bad_blank_data(self):
        """Blank form: Errors will be displayed and site will not be created"""
        response = self.client.post(reverse('streamwebs:create_school'), {})

        self.assertTemplateUsed(response, 'streamwebs/add_school.html')

        self.assertFormError(response, 'school_form', 'name',
                             'This field is required.')

        self.assertFormError(response, 'school_form', 'school_type',
                             'This field is required.')
        self.assertFormError(response, 'school_form', 'address',
                             'This field is required.')
        self.assertFormError(response, 'school_form', 'city',
                             'This field is required.')
        self.assertFormError(response, 'school_form', 'province',
                             'This field is required.')
        self.assertFormError(response, 'school_form', 'zipcode',
                             'This field is required.')

    def test_view_with_good_data(self):
        """When a good form is submitted, good things happen"""

        response = self.client.post(reverse('streamwebs:create_school'), {
            'name': 'Cool School',
            'school_type': 'Organization',
            'address': '1134 nw 23rd st.',
            'city': 'Corvallis',
            'province': 'OR',
            'zipcode': '97330'})

        self.assertTemplateUsed(response, 'streamwebs/index.html')
