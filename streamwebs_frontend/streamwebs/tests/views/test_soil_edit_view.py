from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from streamwebs.models import Site, School, Soil_Survey


class AddSoilSurveyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.site = Site.test_objects.create_site('A site')
        self.expected_fields = ('school', 'date_time', 'weather', 'site',
                                'landscape_pos', 'cover_type', 'land_use',
                                'distance', 'site_char', 'soil_type')
        self.optional_fields = ('site_char')

    def test_view_with_blank_data(self):
        """
        When the user tries to submit a blank form, form errors should be
        displayed
        """
        site = Site.test_objects.create_site('A site')
        response = self.client.post(
            reverse(
                'streamwebs:soil_edit',
                kwargs={'site_slug': site.site_slug}
            ), {}
        )
        self.assertFormError(response, 'soil_form', 'school',
                             'This field is required.')
        self.assertTemplateUsed(response,
                                'streamwebs/datasheets/soil_edit.html')

    def test_edit_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, the user should see a success message
        """
        school = School.test_objects.create_school('rahrahrah')
        response = self.client.post(
            reverse(
                'streamwebs:soil_edit',
                kwargs={'site_slug': self.site.site_slug}
            ), {
                  'school': school.id,
                  'date': '2016-10-19',
                  'time': '03:25',
                  'ampm': 'PM',
                  'weather': 'gray',
                  'landscape_pos': 'summit',
                  'cover_type': 'trees',
                  'land_use': 'wilderness',
                  'distance': '30',
                  'site_char': 'Pretty distinguishable',
                  'notes': 'some notes',
                  'soil_type': 'clay_loam',
                }
        )
        soil = Soil_Survey.objects.order_by('-id')[0]

        self.assertTemplateNotUsed(response,
                                   'streamwebs/datasheets/soil_edit.html')
        self.assertRedirects(response, reverse(
            'streamwebs:soil',
            kwargs={'site_slug': self.site.site_slug, 'data_id': soil.id}),
            status_code=302, target_status_code=200)

    def test_edit_view_with_not_logged_in_user(self):
        """
        When the user is not logged in, they can't add/edit data
        """
        site = Site.test_objects.create_site('A site')
        self.client.logout()
        response = self.client.post(
            reverse(
                'streamwebs:soil_edit',
                kwargs={'site_slug': site.site_slug}
            )
        )
        self.assertRedirects(
            response,
            (reverse('streamwebs:login') + '?next=' +
                reverse('streamwebs:soil_edit',
                        kwargs={'site_slug': site.site_slug})),
            status_code=302,
            target_status_code=200)
