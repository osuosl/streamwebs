from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site, School, Water_Quality, WQ_Sample


class AddWaterQualityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john', 'john@example.com', 'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')
        self.school = School.test_objects.create_school('Test School')

    def test_view_sample(self):
        """ View a sample """
        site = Site.test_objects.create_site('Site Name')
        location = Water_Quality.test_objects.create_water_quality(
            site, u'2016-08-22', self.school,
            u'C', 125.16, 43.12001, u'True', 4, 1,
            u'Fahrenheit', u'Celsius', u"Call your mom on Mothers Day!"
        )
        for i in range(4):
            WQ_Sample.test_objects.create_sample(
                location, u'1', u'27', u'Manual', u'32', u'Vernier', u'1',
                u'Manual', u'5.4', u'Manual', u'10', u'Manual',  u'10',
                u'Manual', 0, 0, 0, 0, 0, 0, 0, 0
            )
        response = self.client.get(
            reverse(
                'streamwebs:water_quality',
                kwargs={
                    'site_slug': site.site_slug,
                    'data_id': location.id,
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/water_quality.html'
        )
        self.assertContains(response, u"Call your mom on Mothers Day!")
