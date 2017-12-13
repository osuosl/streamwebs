from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from streamwebs.models import Site, School, Canopy_Cover, UserProfile


class AddCanopyCoverTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.school = School.test_objects.create_school('Test School')

        self.user = User.objects.create_user(
            'john', 'john@example.com', 'johnpassword'
        )
        self.user.groups.add(Group.objects.get(name='org_admin'))
        self.client.login(username='john', password='johnpassword')

        self.profile = UserProfile()
        self.profile.user = self.user
        self.profile.school = self.school
        self.profile.birthdate = '1123-11-30'
        self.profile.save()

    def test_view_with_bad_blank_data(self):
        """
        Display form errors when the user submits a (completely) blank form
        """
        site = Site.test_objects.create_site('Test')
        response = self.client.post(
            reverse(
                'streamwebs:canopy_cover_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                'canopy_cover-TOTAL_FORMS': '4',
                'canopy_cover-INITIAL_FORMS': '0',
                'canopy_cover-MAX_NUM_FORMS': '4'
               }
        )
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/canopy_cover_edit.html'
        )

    def test_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, return a success message
        """
        site = Site.test_objects.create_site('Testoo')
        response = self.client.post(
            reverse(
                'streamwebs:canopy_cover_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                'date': '2016-08-31',
                'time': '12:30',
                'ampm': 'AM',
                'site': site.id,
                'weather': 'Gray',

                'canopy_cover-TOTAL_FORMS': '8',
                'canopy_cover-INITIAL_FORMS': '0',
                'canopy_cover-MAX_NUM_FORMS': '8',

                'north_cc': 0b1101100101,
                'east_cc': 0b00101010101,
                'south_cc': 0b10010101010,
                'west_cc': 0b01011010101,

                'est_canopy_cover': 49
               }
        )
        self.assertTemplateNotUsed(
            response,
            'streamwebs/datasheets/canopy_cover_edit.html'
        )

        self.assertRedirects(
            response,
            reverse('streamwebs:canopy_cover',
                    kwargs={'site_slug': site.site_slug,
                            'data_id': Canopy_Cover.objects.last().id}
                    ),
            status_code=302,
            target_status_code=200)

    def test_view_with_not_logged_in_user(self):
        """
        When the user isn't logged in, don't display the the data entry page
        """
        self.client.logout()
        site = Site.test_objects.create_site('Test')
        response = self.client.get(
            reverse(
                'streamwebs:canopy_cover_edit',
                kwargs={'site_slug': site.site_slug}
            )
        )
        self.assertTemplateNotUsed(
            response,
            'streamwebs/datasheets/canopy_cover_edit.html'
        )

        self.assertRedirects(
            response,
            (reverse('streamwebs:login') + '?next=' +
                reverse('streamwebs:canopy_cover_edit',
                        kwargs={'site_slug': site.site_slug})),
            status_code=302,
            target_status_code=200)
