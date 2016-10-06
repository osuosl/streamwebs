from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from streamwebs.models import Site, School


class MacroFormTestCase(TestCase):

    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.site = Site.objects.create_site('Site Name!', 'Site Type!')

    def test_edit_view_with_bad_blank_data(self):
        """
        When the user tries to submit a bad (blank) form, the form errors
        should be displayed
        """
        test_site = Site.test_objects.create_site('test site')
        response = self.client.post(
            reverse('streamwebs:macroinvertebrate_edit', kwargs={
                'site_slug': test_site.site_slug
                }), {}
        )
        self.assertFormError(response, 'macro_form', 'school',
                             'This field is required.')
        self.assertFalse(response.context['added'])

    def test_edit_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, the user should see a success message
        """
        test_site = Site.test_objects.create_site('test site')  # NOQA
        test_school = School.test_objects.create_school('test school')

        response = self.client.post(
            reverse('streamwebs:macroinvertebrate_edit', kwargs={
                'site_slug': 'test-site'}), {
                'school': test_school.id,
                'date_time': '2016-07-11 14:09',
                'weather': "aaaa",
                'time_spent': 1,
                'num_people': 2,
                'riffle': True,
                'pool': False,
                'caddisfly': 1,
                'mayfly': 2,
                'riffle_beetle': 1,
                'stonefly': 2,
                'water_penny': 1,
                'dobsonfly': 2,
                'clam_or_mussel': 2,
                'crane_fly': 1,
                'crayfish': 2,
                'damselfly': 1,
                'dragonfly': 2,
                'scud': 1,
                'fishfly': 2,
                'alderfly': 1,
                'mite': 2,
                'aquatic_worm': 2,
                'blackfly': 1,
                'leech': 2,
                'midge': 1,
                'snail': 1,
                'mosquito_larva': 2,
            }
        )
        self.assertTemplateUsed(response,
                                'streamwebs/datasheets/' +
                                'macroinvertebrate_edit.html')
        self.assertTrue(response.context['added'])

        self.assertEqual(response.status_code, 200)

    def test_edit_view_with_not_logged_in_user(self):
        """
        When the user is not logged in, they cannot view the data entry page
        """
        test_site = Site.test_objects.create_site('test site')
        self.client.logout()
        response = self.client.post(
            reverse('streamwebs:macroinvertebrate_edit', kwargs={
                'site_slug': test_site.site_slug
            })
        )
        self.assertContains(response, 'You must be logged in to submit data.')
        self.assertEqual(response.status_code, 200)
