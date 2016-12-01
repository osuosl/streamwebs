from django.test import TestCase
from django.core.urlresolvers import reverse
from streamwebs.models import Site, School, Soil_Survey


class ViewSoilSurveyTestCase(TestCase):
    def setUp(self):
        self.site = Site.test_objects.create_site('Another site')
        self.school = School.test_objects.create_school('rahrahrah')
        self.soil_survey = Soil_Survey.objects.create(
            site=self.site, school=self.school, date='2016-10-20 14:28',
            weather='cloudy', landscape_pos='Stream Bank', cover_type='Shrubs',
            land_use='Other', distance=2,
            site_char='Lots of rocks around', soil_type='Silt Loam')

        self.response = self.client.get(
            reverse(
                'streamwebs:soil',
                kwargs={
                    'data_id': self.soil_survey.id,
                    'site_slug': self.site.site_slug
                }
            )
        )

    def test_data_sheet_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, 'streamwebs/datasheets/soil_view.html'
        )

    def test_data_sheet_view_content(self):
        self.assertContains(self.response, 'Soil Survey')
        self.assertContains(self.response, 'School')
        self.assertContains(self.response, 'Weather')
        self.assertContains(self.response, 'Landscape Position')
        self.assertContains(self.response, 'Cover Type')
        self.assertContains(self.response, 'Land Use')
        self.assertContains(self.response, 'Distance')
        self.assertContains(self.response, 'Site Characteristics')
        self.assertContains(self.response, 'Soil Type')
