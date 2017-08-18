from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, School, Macroinvertebrates


class MacroViewTestCase(TestCase):
    def setUp(self):
        self.site = Site.test_objects.create_site('site name')
        self.school = School.test_objects.create_school('school name')
        self.macro = Macroinvertebrates.test_objects.create_macro(
            self.site, self.school, 2, 3, 'pool', 4, 5, 6, 7, 8, 9, 1, 2, 3, 4,
            5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 'wow, bugs')
        self.response = self.client.get(
            reverse(
                'streamwebs:macroinvertebrate_view',
                kwargs={'data_id': self.macro.id,
                        'site_slug': self.site.site_slug
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
        self.assertContains(self.response, 'wow, bugs')
        self.assertContains(self.response, 'bbbb')
        self.assertContains(self.response, self.macro.site.site_name)
        self.assertContains(self.response, self.macro.school.name)

    def test_wq_rating_adjective(self):
        self.assertEqual(self.response.context['rating'], 'Excellent')

    def test_EPT(self):
        self.assertContains(self.response, 'Percent EPT: 15.24%')
