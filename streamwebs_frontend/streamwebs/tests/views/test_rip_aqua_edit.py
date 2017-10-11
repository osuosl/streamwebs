from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from streamwebs.models import Site, School, RipAquaticSurvey


class CreateRiparianAquaticSurveyTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(username='john', password='johnpassword')
        self.site = Site.test_objects.create_site('hey')

    def test_edit_with_bad_blank_data(self):
        """Blank form: Errors will be displayed and
            site will not be created """
        response = self.client.post(
            reverse('streamwebs:rip_aqua_edit', kwargs={
                'site_slug': self.site.site_slug}))
        self.assertFormError(response, 'rip_aqua_form', 'school',
                             'This field is required.')
        self.assertFormError(response, 'rip_aqua_form', 'school',
                             'This field is required.')

    def test_edit_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, the user should see a success message
        """
        test_school = School.test_objects.create_school('test school')
        site = Site.test_objects.create_site('sup')

        response = self.client.post(reverse(
                'streamwebs:rip_aqua_edit',
                kwargs={'site_slug': site.site_slug}), {
                'school': test_school.id,
                'date': '1996-12-16',
                'time': '2:09',
                'ampm': 'PM',
                'riffle_count': 2,
                'pool_count': 2
                }
        )
        rip = RipAquaticSurvey.test_objects.order_by('-id')[0]
        self.assertRedirects(
            response,
            reverse('streamwebs:rip_aqua_view',
                    kwargs={'site_slug': site.site_slug, 'data_id': rip.id}),
            status_code=302, target_status_code=200)
