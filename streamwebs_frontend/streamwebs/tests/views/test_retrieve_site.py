from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site
import tempfile


class RetrieveSiteTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        location = 'POINT(44.0612385 -121.3846841)'
        image = tempfile.NamedTemporaryFile(suffix='.jpg').name

        self.site = Site.objects.create_site('Test Site', 'AP', 'slug',
            location, 'Test site description', image)

    def test_data_sheet_view(self):
        """Tests that view's status is 200 and correct template is used"""
        response = self.client.get(reverse('streamwebs:site',
            kwargs={'site_slug': self.site.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streamwebs/site_detail.html')

    def test_data_sheet_content(self):
        """Tests that view's content is correct"""
        response = self.client.get(reverse('streamwebs:site',
            kwargs={'site_slug': self.site.id}))
        self.assertContains(response, 'Test Site')
        self.assertContains(response, 'Test site description')
