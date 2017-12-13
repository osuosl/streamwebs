from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from streamwebs.models import School, UserProfile

class CreateSchoolTestCase(TestCase):

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
        """Blank form: Errors will be displayed and site will not be created"""
        response = self.client.post(reverse('streamwebs:create_school'), {})

        self.assertTemplateUsed(response, 'streamwebs/add_school.html')

        self.assertFormError(response, 'school_form', 'name',
                             'This field is required.')

        self.assertFormError(response, 'school_form', 'school_type',
                             'This field is required.')
        self.assertFormError(response, 'school_form', 'address',
                             'This field is required.')
        self.assertFormError(response, 'school_form', 'city',
                             'This field is required.')
        self.assertFormError(response, 'school_form', 'province',
                             'This field is required.')
        self.assertFormError(response, 'school_form', 'zipcode',
                             'This field is required.')
