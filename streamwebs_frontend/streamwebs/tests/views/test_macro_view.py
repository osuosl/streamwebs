from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, Macroinvertebrates


class MacroViewTestCase(TestCase):

    def test_data_sheet_view(self):
        site = Site.objects.create_site('Site Name', 'Site Type', 'site_slug')
        macro = Macroinvertebrates.objects.create_macro(
            site, 1, 2, 3, True, True, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6,
            7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8)

        response = self.client.get(
            reverse(
                'streamwebs:macroinvertebrate',
                kwargs={'data_id': macro.id,
                        'site_slug': macro.site.id
                        }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/macroinvertebrate_view.html'
        )

    def test_data_sheet_view_content(self):
        site = Site.objects.create_site('Site Name', 'Site Type', 'site_slug')
        macro = Macroinvertebrates.objects.create_macro(
            site, 1, 2, 3, True, True, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6,
            7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8)

        response = self.client.get(
            reverse(
                'streamwebs:macroinvertebrate',
                kwargs={'data_id': macro.id,
                        'site_slug': macro.site.id
                        }
            )
        )

        self.assertContains(response, 'macroinvertebrates')
        self.assertContains(response, 'caddisfly')
        self.assertContains(response, 'mayfly')
        self.assertContains(response, 'stonefly')
        self.assertContains(response, 'dobsonfly')
        self.assertContains(response, 'damselfly')
        self.assertContains(response, 'dragonfly')
