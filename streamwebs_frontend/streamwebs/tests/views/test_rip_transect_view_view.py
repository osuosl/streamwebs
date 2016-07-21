from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewTransectTestCase(TestCase):
    def test_data_sheet_view(self):
        response = self.client.get(
            reverse('streamwebs:riparian_transect_view')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/riparian_transect_view.html'
        )
        self.assertContains(response, 'Riparian Transect')
