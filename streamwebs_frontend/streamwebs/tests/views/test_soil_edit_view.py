# from django.test import Client, TestCase
# from django.contrib.auth.models import User, Group
# from django.core.urlresolvers import reverse
# from streamwebs.models import Site, School, Soil_Survey, UserProfile
#
#
# class AddSoilSurveyTestCase(TestCase):
#    def setUp(self):
#
#        self.client = Client()
#
#        self.school = School.test_objects.create_school('Test School')
#
#        self.user = User.objects.create_user(
#            'john', 'john@example.com', 'johnpassword'
#        )
#        self.user.groups.add(Group.objects.get(name='org_admin'))
#        self.client.login(username='john', password='johnpassword')
#
#        self.profile = UserProfile()
#        self.profile.user = self.user
#        self.profile.school = self.school
#        self.profile.save()
#
#        self.site = Site.test_objects.create_site('A site')
#
#    def test_view_with_blank_data(self):
#        """
#        When the user tries to submit a blank form, form errors should be
#        displayed
#        """
#        site = Site.test_objects.create_site('A site')
#        response = self.client.post(
#            reverse(
#                'streamwebs:soil_edit',
#                kwargs={'site_slug': site.site_slug}
#            ), {}
#        )
#        self.assertTemplateUsed(response,
#                                'streamwebs/datasheets/soil_edit.html')
#
#    def test_edit_view_with_good_data(self):
#        """
#        When the user submits a form with all required fields filled
#        appropriately, the user should see a success message
#        """
#        response = self.client.post(
#            reverse(
#                'streamwebs:soil_edit',
#                kwargs={'site_slug': self.site.site_slug}
#            ), {
#                  'date': '2016-10-19',
#                  'time': '03:25',
#                  'ampm': 'PM',
#                  'weather': 'gray',
#                  'landscape_pos': 'summit',
#                  'cover_type': 'trees',
#                  'land_use': 'wilderness',
#                  'distance': '30',
#                  'site_char': 'Pretty distinguishable',
#                  'notes': 'some notes',
#                  'soil_type': 'clay_loam',
#                }
#        )
#        soil = Soil_Survey.objects.order_by('-id')[0]
#
#        self.assertTemplateNotUsed(response,
#                                   'streamwebs/datasheets/soil_edit.html')
#        self.assertRedirects(response, reverse(
#            'streamwebs:soil',
#            kwargs={'site_slug': self.site.site_slug, 'data_id': soil.id}),
#            status_code=302, target_status_code=200)
#
#    def test_edit_view_with_not_logged_in_user(self):
#        """
#        When the user is not logged in, they can't add/edit data
#        """
#        site = Site.test_objects.create_site('A site')
#        self.client.logout()
#        response = self.client.post(
#            reverse(
#                'streamwebs:soil_edit',
#                kwargs={'site_slug': site.site_slug}
#            )
#        )
#        self.assertRedirects(
#            response,
#            (reverse('streamwebs:login') + '?next=' +
#                reverse('streamwebs:soil_edit',
#                        kwargs={'site_slug': site.site_slug})),
#            status_code=302,
#            target_status_code=200)
