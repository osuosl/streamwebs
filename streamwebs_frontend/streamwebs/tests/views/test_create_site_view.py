import tempfile
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class CreateSiteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_view_with_bad_blank_data(self):
        """Blank form: Errors will be displayed and site will not be created"""
        response = self.client.post(reverse('streamwebs:create_site'), {})

        self.assertTemplateUsed(response, 'streamwebs/create_site.html')

        self.assertFormError(response, 'site_form', 'site_name',
                             'This field is required.')
        self.assertFormError(response, 'site_form', 'location',
                             'No geometry value provided.')

        self.assertFalse(response.context['created'])

    def test_view_with_good_data(self):
        """When a good form is submitted, the user sees a success message"""
        temp_photo = tempfile.NamedTemporaryFile(suffix='.jpg').name
        response = self.client.post(reverse('streamwebs:create_site'), {
            'site_name': 'Cool Creek',
            'description': 'A very cool creek',
            'location': 'POINT(-121.3846841 44.0612385)',
            'image': temp_photo})

        self.assertRedirects(response, reverse('streamwebs:site',
                             kwargs={'site_slug': 'cool-creek'}),
                             status_code=302, target_status_code=200)

    def test_view_with_not_logged_in_user(self):
        """Tests that the user can't submit data if they're not logged in"""
        self.client.logout()
        response = self.client.get(reverse('streamwebs:create_site'))

        self.assertContains(response, 'You must be logged in to submit data.')
        self.assertEqual(response.status_code, 200)
