from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from streamwebs.models import Site, School, RipAquaticSurvey, UserProfile


class CreateRiparianAquaticSurveyTestCase(TestCase):

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
        self.profile.save()

        self.site = Site.test_objects.create_site('hey')

    def test_edit_view_with_good_data(self):
        """
        When the user submits a form with all required fields filled
        appropriately, the user should see a success message
        """
        site = Site.test_objects.create_site('sup')

        response = self.client.post(reverse(
                'streamwebs:rip_aqua_edit',
                kwargs={'site_slug': site.site_slug}), {
                'date': '1996-12-16',
                'time': '02:09',
                'ampm': 'PM',
                'riffle_count': 2,
                'pool_count': 2,
                'weather': 'good',
                'silt': 'Some',
                'sand': 'Some',
                'gravel': 'Some',
                'cobble': 'Some',
                'boulders': 'Some',
                'bedrock': 'Some',
                'small_debris': 'Some',
                'medium_debris': 'Some',
                'large_debris': 'Some',
                'comments': "HERRO",
                'coniferous_trees': 'Some',
                'deciduous_trees': 'Some',
                'shrubs': 'Some',
                'small_plants': 'Some',
                'ferns': 'Some',
                'grasses': 'Some',
                'species': 'Some',
                'significance': 'Some',
                'wildlife_type': 'Some',
                'wildlife_comments': 'Some',
                'Notes': 'Some notes'
                }
        )
        rip = RipAquaticSurvey.test_objects.order_by('-id')[0]
        self.assertRedirects(
            response,
            reverse('streamwebs:rip_aqua_view',
                    kwargs={'site_slug': site.site_slug, 'data_id': rip.id}),
            status_code=302, target_status_code=200)
