from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site, School


class AddWaterQualityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john', 'john@example.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')
        self.school = School.test_objects.create_school('Test School')

    def test_view_with_bad_blank_data(self):
        """
        When the user tries to submit a bad (blank) form, the form errors
        should be displayed
        """
        site = Site.test_objects.create_site('Site Name')
        response = self.client.post(
            reverse(
                'streamwebs:water_quality_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                'water_quality-TOTAL_FORMS': '4',
                'water_quality-INITIAL_FORMS': '0',
                'water_quality-MAX_NUM_FORMS': '4'
                }
        )
        self.assertFormError(
            # At least one field should return an error
            response, 'wq_form',
            'fish_present',
            'This field is required.'
        )
        self.assertFalse(response.context['added'])

    def test_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, the user should see a success message
        """
        site = Site.test_objects.create_site('Site Name')
        response = self.client.post(
            reverse(
                'streamwebs:water_quality_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                'DEQ_dq_level': u'A',
                'air_temp_unit': u'Fahrenheit',
                'water_temp_unit': u'Fahrenheit',
                'date': u'2016-08-22',
                'dead_fish': 2,
                'fish_present': u'True',
                'initial-date': u'2016-08-22',
                'latitude': 50,
                'live_fish': 5,
                'longitude': 50,
                'notes': u"Call your mom on Mother's Day!",
                'school': self.school.id,
                'site': site.id,
                'water_quality-0-air_temp_tool': u'Manual',
                'water_quality-0-air_temperature': u'2',
                'water_quality-0-ammonia': u'0',
                'water_quality-0-bod': u'0',
                'water_quality-0-conductivity': u'1',
                'water_quality-0-dissolved_oxygen': u'1',
                'water_quality-0-fecal_coliform': u'0',
                'water_quality-0-nitrate': u'0',
                'water_quality-0-nitrite': u'0',
                'water_quality-0-oxygen_tool': u'Manual',
                'water_quality-0-pH': u'0',
                'water_quality-0-pH_tool': u'Manual',
                'water_quality-0-phosphates': u'2',
                'water_quality-0-salinity': u'0',
                'water_quality-0-salt_tool': u'Vernier',
                'water_quality-0-total_solids': u'0',
                'water_quality-0-turbid_tool': u'Manual',
                'water_quality-0-turbidity': u'0',
                'water_quality-0-water_temp_tool': u'Manual',
                'water_quality-0-water_temperature': u'1',
                'water_quality-1-air_temp_tool': u'Manual',
                'water_quality-1-air_temperature': u'2',
                'water_quality-1-ammonia': u'0',
                'water_quality-1-bod': u'0',
                'water_quality-1-conductivity': u'0',
                'water_quality-1-dissolved_oxygen': u'0',
                'water_quality-1-fecal_coliform': u'3',
                'water_quality-1-nitrate': u'2',
                'water_quality-1-nitrite': u'0',
                'water_quality-1-oxygen_tool': u'Manual',
                'water_quality-1-pH': u'1',
                'water_quality-1-pH_tool': u'Vernier',
                'water_quality-1-phosphates': u'0',
                'water_quality-1-salinity': u'0',
                'water_quality-1-salt_tool': u'Vernier',
                'water_quality-1-total_solids': u'1',
                'water_quality-1-turbid_tool': u'Vernier',
                'water_quality-1-turbidity': u'0',
                'water_quality-1-water_temp_tool': u'Manual',
                'water_quality-1-water_temperature': u'1',
                'water_quality-2-air_temp_tool': u'Vernier',
                'water_quality-2-air_temperature': u'2',
                'water_quality-2-ammonia': u'0',
                'water_quality-2-bod': u'1',
                'water_quality-2-conductivity': u'0',
                'water_quality-2-dissolved_oxygen': u'0',
                'water_quality-2-fecal_coliform': u'0',
                'water_quality-2-nitrate': u'0',
                'water_quality-2-nitrite': u'2',
                'water_quality-2-oxygen_tool': u'Vernier',
                'water_quality-2-pH': u'0',
                'water_quality-2-pH_tool': u'Manual',
                'water_quality-2-phosphates': u'0',
                'water_quality-2-salinity': u'0',
                'water_quality-2-salt_tool': u'Manual',
                'water_quality-2-total_solids': u'0',
                'water_quality-2-turbid_tool': u'Manual',
                'water_quality-2-turbidity': u'1',
                'water_quality-2-water_temp_tool': u'Vernier',
                'water_quality-2-water_temperature': u'1',
                'water_quality-3-air_temp_tool': u'Vernier',
                'water_quality-3-air_temperature': u'2',
                'water_quality-3-ammonia': u'1',
                'water_quality-3-bod': u'0',
                'water_quality-3-conductivity': u'0',
                'water_quality-3-dissolved_oxygen': u'0',
                'water_quality-3-fecal_coliform': u'0',
                'water_quality-3-nitrate': u'0',
                'water_quality-3-nitrite': u'0',
                'water_quality-3-oxygen_tool': u'Vernier',
                'water_quality-3-pH': u'0',
                'water_quality-3-pH_tool': u'Vernier',
                'water_quality-3-phosphates': u'0',
                'water_quality-3-salinity': u'1',
                'water_quality-3-salt_tool': u'Manual',
                'water_quality-3-total_solids': u'0',
                'water_quality-3-turbid_tool': u'Vernier',
                'water_quality-3-turbidity': u'0',
                'water_quality-3-water_temp_tool': u'Vernier',
                'water_quality-3-water_temperature': u'1',
                'water_quality-TOTAL_FORMS': '4',
                'water_quality-INITIAL_FORMS': '0',
                'water_quality-MAX_NUM_FORMS': '4'
            }
        )
        self.assertTemplateUsed(
            response, 'streamwebs/datasheets/water_quality.html'
        )
        self.assertTrue(response.context['added'])
        self.assertEqual(response.status_code, 200)

    def test_view_with_not_logged_in_user(self):
        """
        When the user is not logged in, they cannot view the data entry page
        """
        self.client.logout()
        site = Site.test_objects.create_site('Site Name')
        response = self.client.get(
            reverse(
                'streamwebs:water_quality_edit',
                kwargs={'site_slug': site.site_slug}
            )
        )
        self.assertRedirects(
            response,
            (reverse('streamwebs:login') + '?next=' +
                reverse('streamwebs:water_quality_edit',
                        kwargs={'site_slug': site.site_slug})),
            status_code=302,
            target_status_code=200)
