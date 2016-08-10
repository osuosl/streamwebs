from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, Macroinvertebrates


class MacroViewTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.create_site(
            'Site Name', 'Site Type', 'site_slug'
            )
        self.macro = Macroinvertebrates.objects.create_macro(
            self.site, 2, 3, True, True, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5,
            6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8)
        self.response = self.client.get(
            reverse(
                'streamwebs:macroinvertebrate_view',
                kwargs={'data_id': self.macro.id,
                        'site_slug': self.macro.site.id
                        }
            )
        )

    def test_data_sheet_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response,
            'streamwebs/datasheets/macroinvertebrate_view.html'
        )

    def test_data_sheet_view_content(self):
        self.assertContains(self.response, 'Macroinvertebrates')
        self.assertContains(self.response, 'caddisfly')
        self.assertContains(self.response, 'mayfly')
        self.assertContains(self.response, 'stonefly')
        self.assertContains(self.response, 'dobsonfly')
        self.assertContains(self.response, 'damselfly')
        self.assertContains(self.response, 'dragonfly')