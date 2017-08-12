from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from streamwebs.models import Site, School, RiparianTransect, TransectZone


class AddTransectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'john@example.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.school = School.test_objects.create_school('Test School')

    def test_view_with_bad_blank_data(self):
        """When bad (blank) form submitted, form errors should be displayed"""
        site = Site.test_objects.create_site('Site Name')

        # No riparian transect or zone objects should be created.
        self.assertFalse(
            RiparianTransect.objects.filter(site=site.id).exists())
        self.assertEquals(
            TransectZone.objects.filter(transect__site=site.id).count(), 0)

    def test_view_with_valid_zones(self):
        """If all zones completely filled in, data sheet is certainly valid"""
        site = Site.test_objects.create_site('Site Name')
        response = self.client.post(
            reverse(
                'streamwebs:riparian_transect_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                    'school': self.school.id,
                    'date_time': '2016-07-18 14:09:07',
                    'weather': 'cloudy',
                    'site': site.id,
                    'slope': 5,
                    'notes': 'notes',

                    'transect-TOTAL_FORMS': '5',
                    'transect-INITIAL_FORMS': '0',
                    'transect-MAX_NUM_FORMS': '5',

                    'transect-0-conifers': 1,
                    'transect-0-hardwoods': 2,
                    'transect-0-shrubs': 3,
                    'transect-0-comments': '1 comments',

                    'transect-1-conifers': 4,
                    'transect-1-hardwoods': 5,
                    'transect-1-shrubs': 6,
                    'transect-1-comments': '2 comments',

                    'transect-2-conifers': 7,
                    'transect-2-hardwoods': 8,
                    'transect-2-shrubs': 9,
                    'transect-2-comments': '3 comments',

                    'transect-3-conifers': 8,
                    'transect-3-hardwoods': 7,
                    'transect-3-shrubs': 6,
                    'transect-3-comments': '4 comments',

                    'transect-4-conifers': 5,
                    'transect-4-hardwoods': 4,
                    'transect-4-shrubs': 3,
                    'transect-4-comments': '5 comments'
                }
        )
        self.assertRedirects(
            response,
            reverse('streamwebs:riparian_transect',
                    kwargs={'site_slug': site.site_slug,
                            'data_id': RiparianTransect.test_objects.last().id}
                    ),
            status_code=302,
            target_status_code=200)

        # Transect object and all five of its zones should have been created.
        self.assertTrue(
            RiparianTransect.objects.filter(site=site.id).exists())
        self.assertEquals(
            TransectZone.objects.filter(transect__site=site.id).count(), 5)

    def test_view_with_bare_minimum(self):
        """If one zone has at least one nonzero val: all 5 zones get created"""
        site = Site.test_objects.create_site('Site Name!')
        response = self.client.post(
            reverse(
                'streamwebs:riparian_transect_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                    'school': self.school.id,
                    'date_time': '2016-07-18 14:09:07',
                    'weather': 'cloudy',
                    'site': site.id,
                    'slope': 5,
                    'notes': 'notes',

                    'transect-TOTAL_FORMS': '5',
                    'transect-INITIAL_FORMS': '0',
                    'transect-MAX_NUM_FORMS': '5',

                    'transect-0-conifers': 0,
                    'transect-0-hardwoods': 0,
                    'transect-0-shrubs': 0,
                    'transect-0-comments': '',

                    'transect-1-conifers': 0,
                    'transect-1-hardwoods': 0,
                    'transect-1-shrubs': 0,
                    'transect-1-comments': '',

                    'transect-2-conifers': 0,
                    'transect-2-hardwoods': 1,
                    'transect-2-shrubs': 0,
                    'transect-2-comments': '',

                    'transect-3-conifers': 0,
                    'transect-3-hardwoods': 0,
                    'transect-3-shrubs': 0,
                    'transect-3-comments': '',

                    'transect-4-conifers': 0,
                    'transect-4-hardwoods': 0,
                    'transect-4-shrubs': 0,
                    'transect-4-comments': ''
                }
        )
        self.assertRedirects(
            response,
            reverse('streamwebs:riparian_transect',
                    kwargs={'site_slug': site.site_slug,
                            'data_id': RiparianTransect.test_objects.last().id}
                    ),
            status_code=302,
            target_status_code=200)

        self.assertTrue(
            RiparianTransect.objects.filter(site=site.id).exists())
        self.assertEquals(
            TransectZone.objects.filter(transect__site=site.id).count(), 5)

    def test_view_with_invalid_zones_with_notes(self):
        """When counts for all zones are 0, can't submit even if notes exist"""
        site = Site.test_objects.create_site('Bad Transect with Notes')
        response = self.client.post(
            reverse(
                'streamwebs:riparian_transect_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                    'school': self.school.id,
                    'date_time': '2016-07-18 14:09:07',
                    'weather': 'cloudy',
                    'site': site.id,
                    'slope': 5,
                    'notes': 'notes',

                    'transect-TOTAL_FORMS': '5',
                    'transect-INITIAL_FORMS': '0',
                    'transect-MAX_NUM_FORMS': '5',

                    'transect-0-conifers': 0,
                    'transect-0-hardwoods': 0,
                    'transect-0-shrubs': 0,
                    'transect-0-comments': '',

                    'transect-1-conifers': 0,
                    'transect-1-hardwoods': 0,
                    'transect-1-shrubs': 0,
                    'transect-1-comments': '2 comments',

                    'transect-2-conifers': 0,
                    'transect-2-hardwoods': 0,
                    'transect-2-shrubs': 0,
                    'transect-2-comments': '',

                    'transect-3-conifers': 0,
                    'transect-3-hardwoods': 0,
                    'transect-3-shrubs': 0,
                    'transect-3-comments': '4 comments',

                    'transect-4-conifers': 0,
                    'transect-4-hardwoods': 0,
                    'transect-4-shrubs': 0,
                    'transect-4-comments': '5 comments'
                    }
        )
        self.assertTemplateUsed(
            response,
            'streamwebs/datasheets/riparian_transect_edit.html')
        self.assertTemplateNotUsed(
            response,
            'streamwebs/datasheets/riparian_transect_view.html')

        self.assertFalse(
            RiparianTransect.objects.filter(site=site.id).exists())
        self.assertEquals(
            TransectZone.objects.filter(transect__site=site.id).count(), 0)

    def test_view_with_invalid_zones_without_notes(self):
        """Can't submit when all zones completely blank/zeroed out"""
        site = Site.test_objects.create_site('Bad Transect without Notes')
        response = self.client.post(
            reverse(
                'streamwebs:riparian_transect_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                    'school': self.school.id,
                    'date_time': '2016-07-18 14:09:07',
                    'weather': 'cloudy',
                    'site': site.id,
                    'slope': 5,
                    'notes': 'notes',

                    'transect-TOTAL_FORMS': '5',
                    'transect-INITIAL_FORMS': '0',
                    'transect-MAX_NUM_FORMS': '5',

                    'transect-0-conifers': 0,
                    'transect-0-hardwoods': 0,
                    'transect-0-shrubs': 0,
                    'transect-0-comments': '',

                    'transect-1-conifers': 0,
                    'transect-1-hardwoods': 0,
                    'transect-1-shrubs': 0,
                    'transect-1-comments': '',

                    'transect-2-conifers': 0,
                    'transect-2-hardwoods': 0,
                    'transect-2-shrubs': 0,
                    'transect-2-comments': '',

                    'transect-3-conifers': 0,
                    'transect-3-hardwoods': 0,
                    'transect-3-shrubs': 0,
                    'transect-3-comments': '',

                    'transect-4-conifers': 0,
                    'transect-4-hardwoods': 0,
                    'transect-4-shrubs': 0,
                    'transect-4-comments': ''
                }
        )
        self.assertTemplateNotUsed(
            response,
            'streamwebs/datasheets/riparian_transect_view.html')

        # No riparian transect or zone objects should be created.
        self.assertFalse(
            RiparianTransect.objects.filter(site=site.id).exists())
        self.assertEquals(
            TransectZone.objects.filter(transect__site=site.id).count(), 0)

    def test_zone_nums_correctly_assigned(self):
        """Zones should retain their order even if some of them are 'blank'"""
        site = Site.test_objects.create_site('Site Name')
        response = self.client.post(
            reverse(
                'streamwebs:riparian_transect_edit',
                kwargs={'site_slug': site.site_slug}
            ), {
                    'school': self.school.id,
                    'date_time': '2016-07-18 14:09:07',
                    'weather': 'cloudy',
                    'site': site.id,
                    'slope': 5,
                    'notes': 'notes',

                    'transect-TOTAL_FORMS': '5',
                    'transect-INITIAL_FORMS': '0',
                    'transect-MAX_NUM_FORMS': '5',

                    'transect-0-conifers': 0,
                    'transect-0-hardwoods': 0,
                    'transect-0-shrubs': 0,
                    'transect-0-comments': '',

                    'transect-1-conifers': 0,
                    'transect-1-hardwoods': 0,
                    'transect-1-shrubs': 0,
                    'transect-1-comments': 'second zone',

                    'transect-2-conifers': 0,
                    'transect-2-hardwoods': 0,
                    'transect-2-shrubs': 0,
                    'transect-2-comments': '',

                    'transect-3-conifers': 0,
                    'transect-3-hardwoods': 0,
                    'transect-3-shrubs': 1,
                    'transect-3-comments': 'the only good zone',

                    'transect-4-conifers': 0,
                    'transect-4-hardwoods': 0,
                    'transect-4-shrubs': 0,
                    'transect-4-comments': ''
                }
        )
        self.assertRedirects(
            response,
            reverse('streamwebs:riparian_transect',
                    kwargs={'site_slug': site.site_slug,
                            'data_id': RiparianTransect.test_objects.last().id}
                    ),
            status_code=302,
            target_status_code=200)

        # Transect object and all five of its zones should have been created.
        self.assertTrue(
            RiparianTransect.objects.filter(site=site.id).exists())
        self.assertEquals(
            TransectZone.objects.filter(transect__site=site.id).count(), 5)

        # Check that the freshly created zones are correctly associated with
        # their respective zone numbers
        for i in range(5):
            self.assertEquals(TransectZone.objects.order_by('id')[i].zone_num,
                              str(i + 1))

        self.assertEquals(TransectZone.objects.order_by('-id')[4].comments, '')
        self.assertEquals(TransectZone.objects.order_by('-id')[3].comments,
                          'second zone')
        self.assertEquals(TransectZone.objects.order_by('-id')[2].comments, '')
        self.assertEquals(TransectZone.objects.order_by('-id')[1].comments,
                          'the only good zone')
        self.assertEquals(TransectZone.objects.order_by('-id')[0].comments, '')

    def test_view_with_not_logged_in_user(self):
        """
        When the user is not logged in, they cannot view the data entry page
        """
        self.client.logout()
        site = Site.test_objects.create_site('Site Name')
        response = self.client.get(
            reverse(
                'streamwebs:riparian_transect_edit',
                kwargs={'site_slug': site.site_slug}
            )
        )
        self.assertRedirects(
            response,
            (reverse('streamwebs:login') + '?next=' +
                reverse('streamwebs:riparian_transect_edit',
                        kwargs={'site_slug': site.site_slug})),
            status_code=302,
            target_status_code=200)
