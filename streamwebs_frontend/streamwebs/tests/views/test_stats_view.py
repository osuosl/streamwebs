from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, Permission
from streamwebs.models import Site, School, Soil_Survey, RiparianTransect, Canopy_Cover
import datetime


class AdminStatsTestCase(TestCase):
    fixtures = ['sample_users.json', 'sample_sites.json',
                'sample_schools.json', 'sample_transects.json',
                'sample_soil.json', 'sample_canopies.json']

    def setUp(self):
        self.today = datetime.date.today()
        self.client = Client()
        self.reg_user = User.objects.create_user('reg', 'reg@example.com',
                                                 'regpassword')
        self.client.login(username='reg', password='regpassword')
#        self.admin_user = User.objects.create_user('admin',
#                                                   'admin@example.com',
#                                                    'adminpassword')
#        admins = Group.objects.get(name='admin')
#        self.admin_user.groups.set([admins])    # add test admin user to group

        # a school or a site is inactive if it has 0 sheets.
        # if it has at least 1 sheet it should be considered active.

        self.expected_user_stats = {
            'default': ('aithai', 'KANYE_WEST', 'root'),
            'just_start': ('KANYE_WEST', 'root'),
            'just_end': ('randy_savage', 'harambe', 'annilee', 'aithai',
                         'freenode'),
            'range': ('KANYE_WEST',),
        }

        self.expected_sheet_stats = {
            'default': {'total': 60, 'soil': 29, 'transect': 17, 'camera': 0,
                        'macro': 0, 'canopy': 14, 'water': 0},
            'just_start': {'total': 49, 'soil': 25, 'transect': 12,
                           'camera': 0, 'macro': 0, 'canopy': 12, 'water': 0},
            'just_end': {'total': 11, 'soil': 4, 'transect': 5, 'camera': 0,
                         'macro': 0, 'canopy': 2, 'water':0},
            'range': {'total': 29, 'soil': 15, 'transect': 8, 'camera': 0,
                      'macro': 0, 'canopy': 6, 'water': 0}
        }

        blair = Site.objects.get(id=35)
        hamilton = Site.objects.get(id=86)
        belmont = Site.objects.get(id=188)

        self.expected_site_stats = {
            'default': {'total': 3, 'sites': set((blair, hamilton, belmont))},
            'just_start': {'total': 3, 'sites': set((hamilton, belmont,
                                                     blair))},
            'just_end': {'total': 2, 'sites': set((blair, belmont))},
            'range': {'total': 3, 'sites': set((belmont, hamilton, blair))}
        }

        AC = School.objects.get(id=1)
        abernethy = School.objects.get(id=2)
        abraham = School.objects.get(id=3)
        character = School.objects.get(id=4)
        arts = School.objects.get(id=5)
        international = School.objects.get(id=6)
        ace = School.objects.get(id=7)
        ackerman = School.objects.get(id=8)
        # Schools 9 and 10 have no data sheets.

        self.expected_school_stats = {
            'default': {'total': 8, 'schools': set((AC, abernethy, abraham,
                                                    character, arts,
                                                    international, ace,
                                                    ackerman))},
            'just_start': {'total': 8, 'schools': set((AC, abernethy, abraham,
                                                       character, arts,
                                                       international, ace,
                                                       ackerman))},
            'just_end': {'total': 3, 'schools': set((character, international,
                                                     AC))},
            'range': {'total': 8, 'schools': set((AC, abernethy, abraham,
                                                  character, arts,
                                                  international, ace,
                                                  ackerman))}
        }

    def test_data_loaded_and_usable(self):
        sites = Site.objects.all()
        self.assertEquals(sites.count(), 11)
        schools = School.objects.all()
        self.assertEquals(schools.count(), 10)
        transects = RiparianTransect.objects.all()
        self.assertEquals(transects.count(), 17)
        soil = Soil_Survey.objects.all()
        self.assertEquals(soil.count(), 29)
        canopy = Canopy_Cover.objects.all()
        self.assertEquals(canopy.count(), 14)
#
#    def test_admin_user(self):
#        user = User.objects.get(username='root')
##        group = Group.objects.get(name='admin')
##        self.assertEquals(group.name, user.groups)
#        self.assertTrue(user.groups.filter(name='admin').exists())
#
#    def test_not_logged_in_user(self):
#        """If user is not logged in, can't view the stats page, period"""
#        response = self.client.get(reverse('streamwebs:stats'))
#        self.assertRedirects(
#            response,
#            (reverse('streamwebs:login') + '?next=' +
#                reverse('streamwebs:stats')),
#            status_code=302,
#            target_status_code=200)
#
#    def test_admin_user_has_stats_perm(self):
#        """User in admin group with stats perm should be able to view stats"""
#        self.client.login(username='admin', password='adminpassword')
##
#    def test_admin_user_no_stats_perm(self):
#        """User in admin group but without stats perm can't view stats"""
#        self.client.login(username='admin', password='adminpassword')
##        self.assertRaises
## https://docs.djangoproject.com/en/1.10/topics/auth/default/#the-permission-required-decorator
#
#    def test_reg_user_has_stats_perm(self):
#        """Reg user that has stats perm can still view the stats page"""
#        self.client.login(username='reg', password='regpassword')
#
#    def test_reg_user_does_not_have_stats_perm(self):
#        """Reg user without stats perm should be denied access to the page"""
#        self.client.login(username='reg', password='regpassword')
#        self.assertContains("Access denied")

    def test_default_stats_post(self):
        """No start/end provided: Currently active users (3 yrs) returned"""
        response = self.client.post(reverse('streamwebs:stats'), {})
        self.assertEquals(str(response.context['user_start']),
                          str(datetime.date(self.today.year - 3,
                                            self.today.month, self.today.day)))
        self.assertEquals(str(response.context['start']),
                          str(datetime.date(1970, 1, 1)))
        self.assertEquals(str(response.context['end']), str(self.today))
        self.assertTrue(response.context['all_time'])
        self.assertEquals(response.context['users']['count'],
                          len(self.expected_user_stats['default']))
        for user in response.context['users']['users']:
            self.assertIn(user.username, self.expected_user_stats['default'])
            self.assertTrue(user.last_login.date() <= self.today and
                            user.last_login.date() >= datetime.date(
                                self.today.year-3, self.today.month,
                                self.today.day))
        self.assertEquals(response.context['sheets'],
                          self.expected_sheet_stats['default'])
        self.assertEquals(response.context['sites'],
                          self.expected_site_stats['default'])
        self.assertEquals(response.context['schools'],
                          self.expected_school_stats['default'])

    def test_default_stats_get(self):
        """No start/end provided: Currently active users (3 yrs) returned"""
        response = self.client.get(reverse('streamwebs:stats'))
        self.assertEquals(str(response.context['user_start']),
                          str(datetime.date(self.today.year - 3,
                                            self.today.month, self.today.day)))
        self.assertEquals(str(response.context['start']),
                          str(datetime.date(1970, 1, 1)))
        self.assertEquals(str(response.context['end']), str(self.today))
        self.assertTrue(response.context['all_time'])
        self.assertEquals(response.context['users']['count'],
                          len(self.expected_user_stats['default']))
        for user in response.context['users']['users']:
            self.assertIn(user.username, self.expected_user_stats['default'])
            self.assertTrue(user.last_login.date() <= self.today and
                            user.last_login.date() >= datetime.date(
                                self.today.year-3, self.today.month,
                                self.today.day))
        self.assertEquals(response.context['sheets'],
                          self.expected_sheet_stats['default'])
        self.assertEquals(response.context['sites'],
                          self.expected_site_stats['default'])
        self.assertEquals(response.context['schools'],
                          self.expected_school_stats['default'])

    def test_just_start_provided(self):
        """Just start provided: users who joined b/w start to today returned"""
        response = self.client.post(reverse('streamwebs:stats'), {
            'start': datetime.date(2014, 1, 1)})
        self.assertEquals(str(response.context['start']),
                          str(datetime.date(2014, 1, 1)))
        self.assertEquals(str(response.context['end']), str(self.today))
        self.assertFalse(response.context['all_time'])
        self.assertEquals(response.context['users']['count'],
                          len(self.expected_user_stats['just_start']))
        for user in response.context['users']['users']:
            self.assertIn(user.username,
                          self.expected_user_stats['just_start'])
            self.assertTrue(user.date_joined.date() <= self.today and
                            user.date_joined.date() >=
                            datetime.date(2014, 1, 1))
        self.assertEquals(response.context['sheets'],
                          self.expected_sheet_stats['just_start'])
        self.assertEquals(response.context['sites'],
                          self.expected_site_stats['just_start'])
        self.assertEquals(response.context['schools'],
                          self.expected_school_stats['just_start'])

    def test_just_end_provided(self):
        """Just end provided: users who joined b/w end to today returned"""
        response = self.client.post(reverse('streamwebs:stats'), {
            'end': datetime.date(2014, 1, 1)})
        self.assertEquals(str(response.context['end']),
                          str(datetime.date(2014, 1, 1)))
        self.assertEquals(str(response.context['start']),
                          str(datetime.date(1970, 1, 1)))
        self.assertFalse(response.context['all_time'])
        self.assertEquals(response.context['users']['count'],
                          len(self.expected_user_stats['just_end']))
        for user in response.context['users']['users']:
            self.assertIn(user.username,
                          self.expected_user_stats['just_end'])
            self.assertTrue(user.date_joined.date() >=
                            datetime.date(1970, 1, 1) and
                            user.date_joined.date() <=
                            datetime.date(2014, 1, 1))
        self.assertEquals(response.context['sheets'],
                          self.expected_sheet_stats['just_end'])
        self.assertEquals(response.context['sites'],
                          self.expected_site_stats['just_end'])
        self.assertEquals(response.context['schools'],
                          self.expected_school_stats['just_end'])

    def test_range_provided(self):
        """Both start/end provided: users joined b/w start to end returned"""
        response = self.client.post(reverse('streamwebs:stats'), {
            'start': datetime.date(2014, 1, 1),
            'end': datetime.date(2016, 1, 1)})
        self.assertEquals(str(response.context['start']),
                          str(datetime.date(2014, 1, 1)))
        self.assertEquals(str(response.context['end']),
                          str(datetime.date(2016, 1, 1)))
        self.assertFalse(response.context['all_time'])
        self.assertEquals(response.context['users']['count'],
                          len(self.expected_user_stats['range']))
        for user in response.context['users']['users']:
            self.assertIn(user.username,
                          self.expected_user_stats['range'])
            self.assertTrue(user.date_joined.date() <=
                            datetime.date(2016, 1, 1) and
                            user.date_joined.date() >=
                            datetime.date(2014, 1, 1))
        self.assertEquals(response.context['sheets'],
                          self.expected_sheet_stats['range'])
        self.assertEquals(response.context['sites'],
                          self.expected_site_stats['range'])
        self.assertEquals(response.context['schools'],
                          self.expected_school_stats['range'])
