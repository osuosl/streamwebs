from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site
import tempfile


class RetrieveSiteTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.location = 'POINT(44.0612385 -121.3846841)'
        self.image = tempfile.NamedTemporaryFile(suffix='.jpg').name

        # Make a bunch of WQ objects tied to same site
        # When retrieve that site, list of WQ objects should appear

    def test_data_sheet_view(self):
        """Tests that view's status is 200 and correct template is used"""
        site = Site.test_objects.create_site('Test Site', 'AP', 'slug',
                                        self.location, 'Test site description',
                                        self.image)
        response = self.client.get(reverse('streamwebs:site',
                                           kwargs={'site_slug': site.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamwebs/site_detail.html')

    def test_data_sheet_content(self):
        """Tests that view's content is correct"""
        site = Site.test_objects.create_site('Test Site', 'AP', 'slug',
                                        self.location, 'Test site description',
                                        self.image)

        response = self.client.get(reverse('streamwebs:site',
                                           kwargs={'site_slug': site.id}))
        self.assertContains(response, 'Test Site')
        self.assertContains(response, 'Test site description')
