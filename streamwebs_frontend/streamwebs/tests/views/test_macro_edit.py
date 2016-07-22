from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from streamwebs.models import Site


class MacroFormTestCase(TestCase):

    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.site = Site.objects.create_site('Site Name!', 'Site Type!',
                                             'site_slug')
        self.expected_fields = ('school', 'date_time', 'weather', 'site',
                                'time_spent', 'num_people', 'riffle', 'pool',
                                'caddisfly', 'mayfly', 'riffle_beetle',
                                'stonefly', 'water_penny', 'dobsonfly',
                                'sensitive_total', 'clam_or_mussel',
                                'crane_fly', 'crayfish', 'damselfly',
                                'dragonfly', 'scud', 'fishfly', 'alderfly',
                                'mite', 'somewhat_sensitive_total',
                                'aquatic_worm', 'blackfly', 'leech', 'midge',
                                'snail', 'mosquito_larva', 'tolerant_total',
                                'wq_rating')

    def test_edit_view_with_bad_blank_data(self):
        """
        When the user tries to submit a bad (blank) form, the form errors
        should be displayed
        """
        test_site = Site.objects.create_site('test site', 'test site type',
                                             'test_site_slug')
        response = self.client.post(
            reverse('streamwebs:macroinvertebrate_edit', kwargs={
                'site_slug': test_site.id}), {}
        )
        self.assertFormError(response, 'macro_form', 'school',
                             'This field is required.')
        self.assertFalse(response.context['added'])

    def test_edit_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, the user should see a success message
        """
        # TODO MAKE samlpe site
        test_site = Site.objects.create_site('test site', 'test site type',
                                             'test_site_slug')
        response = self.client.post(
            reverse('streamwebs:macroinvertebrate_edit', kwargs={
                'site_slug': test_site.id}), {
                'conifers': 1,
                'school': "aaaa",
                'date_time': '2016-07-11 14:09',
                'weather': "aaaa",
                'site': test_site.id,
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
                'sensitive_total': 27,
                'clam_or_mussel': 2,
                'crane_fly': 1,
                'crayfish': 2,
                'damselfly': 1,
                'dragonfly': 2,
                'scud': 1,
                'fishfly': 2,
                'alderfly': 1,
                'mite': 2,
                'somewhat_sensitive_total': 28,
                'aquatic_worm': 2,
                'blackfly': 1,
                'leech': 2,
                'midge': 1,
                'snail': 1,
                'mosquito_larva': 2,
                'tolerant_total': 9,
                'wq_rating': 64,
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
        test_site = Site.objects.create_site('test site', 'test site type',
                                             'test_site_slug')
        self.client.logout()
        response = self.client.post(
            reverse('streamwebs:macroinvertebrate_edit', kwargs={
                'site_slug': test_site.id}))
        self.assertContains(response, 'You must be logged in to submit data.')
        self.assertEqual(response.status_code, 200)
