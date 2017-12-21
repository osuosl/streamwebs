# TODO
# from django.test import Client, TestCase
# from django.contrib.auth.models import User, Group
# from django.core.urlresolvers import reverse
# from streamwebs.models import Site, School, Macroinvertebrates, UserProfile
#
#
# class MacroFormTestCase(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#
#         self.school = School.test_objects.create_school('Test School')
#
#         self.user = User.objects.create_user(
#             'john', 'john@example.com', 'johnpassword'
#         )
#         self.user.groups.add(Group.objects.get(name='org_admin'))
#         self.client.login(username='john', password='johnpassword')
#
#         self.profile = UserProfile()
#         self.profile.user = self.user
#         self.profile.school = self.school
#         self.profile.save()
#
#         self.site = Site.test_objects.create_site('Site Name!')
#
#     def test_correct_categories_rendered(self):
#         """Tests that the form slices rendered contain the correct macros"""
#         response = self.client.get(
#             reverse('streamwebs:macroinvertebrate_edit', kwargs={
#                 'site_slug': self.site.site_slug}))
#
#         self.assertEqual(response.context['intolerant'][0].label, 'Caddisfly')
#         self.assertEqual(response.context['intolerant'][5].label, 'Dobsonfly')
#         self.assertEqual(response.context['somewhat'][0].label, 'Clam/mussel')
#         self.assertEqual(response.context['somewhat'][8].label, 'Mite')
#         self.assertEqual(response.context['tolerant'][0].label, 'Aquatic worm')
#         self.assertEqual(response.context['tolerant'][5].label,
#                          'Mosquito larva')
#
#     def test_edit_view_with_bad_blank_data(self):
#         """
#         When the user tries to submit a bad (blank) form, the form errors
#         should be displayed
#         """
#         response = self.client.post(
#             reverse('streamwebs:macroinvertebrate_edit', kwargs={
#                 'site_slug': self.site.site_slug
#                 }), {}
#         )
#
#         self.assertFalse(response.context['added'])
#
#     def test_edit_view_with_good_data(self):
#         """
#         When the user submits a form with all required fields filled
#         appropriately, the user should see a success message
#         """
#
#         response = self.client.post(
#             reverse('streamwebs:macroinvertebrate_edit', kwargs={
#                 'site_slug': self.site.site_slug}), {
#                 'date': '2016-07-11',
#                 'time': '02:09',
#                 'ampm': 'PM',
#                 'weather': "aaaa",
#                 'time_spent': 1,
#                 'num_people': 2,
#                 'water_type': 'riff',
#                 'caddisfly': 1,
#                 'mayfly': 2,
#                 'riffle_beetle': 1,
#                 'stonefly': 2,
#                 'water_penny': 1,
#                 'dobsonfly': 2,
#                 'clam_or_mussel': 2,
#                 'crane_fly': 1,
#                 'crayfish': 2,
#                 'damselfly': 1,
#                 'dragonfly': 2,
#                 'scud': 1,
#                 'fishfly': 2,
#                 'alderfly': 1,
#                 'mite': 2,
#                 'aquatic_worm': 2,
#                 'blackfly': 1,
#                 'leech': 2,
#                 'midge': 1,
#                 'snail': 1,
#                 'mosquito_larva': 2,
#                 'notes': ''
#             }
#         )
#         macro = Macroinvertebrates.test_objects.order_by('-id')[0]
#
#         self.assertRedirects(response, reverse(
#             'streamwebs:macroinvertebrate_view',
#             kwargs={'site_slug': self.site.site_slug, 'data_id': macro.id}),
#             status_code=302, target_status_code=200)
#
#     def test_edit_view_with_not_logged_in_user(self):
#         """
#         When the user is not logged in, they cannot view the data entry page
#         """
#         self.client.logout()
#         response = self.client.post(
#             reverse('streamwebs:macroinvertebrate_edit', kwargs={
#                 'site_slug': self.site.site_slug
#             })
#         )
#         self.assertRedirects(response,
#                              reverse('streamwebs:login') + '?next=' + reverse(
#                                  'streamwebs:macroinvertebrate_edit',
#                                  kwargs={'site_slug': self.site.site_slug}),
#                              status_code=302, target_status_code=200)
