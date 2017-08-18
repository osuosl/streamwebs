from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group, Permission
from streamwebs.models import Resource
from streamwebs.util.create_dummy_files import (get_temporary_image,
                                                get_temporary_text_file)


class UploadResourceTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        # regular user with no special permissions
        self.reg_user = User.objects.create_user('reg_user', 'reg@example.com',
                                                 'regpassword')

        # regular user with the "can upload resources" permission
        self.special_user = User.objects.create_user('special_user',
                                                     'special@example.com',
                                                     'specialpassword')
        can_upload = Permission.objects.get(codename='can_upload_resources')
        self.special_user.user_permissions.add(can_upload)

        # admin user with admin permissions (stats and resources)
        admins = Group.objects.get(name='admin')
        self.admin = User.objects.create_user('admin', 'admin@example.com',
                                              'adminpassword')
        self.admin.groups.add(admins)   # add test admin user to group

        # dummy files
        self.temp_file = get_temporary_text_file()
        self.temp_img = get_temporary_image()

    def test_not_logged_in_user(self):
        """If user is not logged in, can't view the upload page or link"""
        # Can't access upload page:
        response = self.client.get(reverse('streamwebs:resources-upload'))
        self.assertRedirects(
            response,
            (reverse('streamwebs:login') + '?next=' +
                reverse('streamwebs:resources-upload')),
            status_code=302,
            target_status_code=200)
        self.assertTemplateNotUsed(
            response, 'streamwebs/resources/resources-upload.html')

        # Can't view link on resources page:
        response = self.client.get(reverse('streamwebs:resources'))
        self.assertContains(
            response,
            "StreamWebs offers a number of resources to get you started in " +
            "the field")
        self.assertNotContains(response, "Upload a new resource")

    def test_admin_user_has_upload_perm(self):
        """User in admin group with upload perm should be able to view page"""
        self.client.login(username='admin', password='adminpassword')
        self.assertTrue(self.admin.has_perms(
            ['streamwebs.can_upload_resources', 'streamwebs.can_view_stats']))
        self.assertTrue(self.admin.groups.filter(name='admin').exists())
        response = self.client.get(reverse('streamwebs:resources-upload'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'streamwebs/resources/resources_upload.html')
        self.assertContains(response, 'Upload a new resource')

        """Should also be able to view link in resources.html"""
        response = self.client.get(reverse('streamwebs:resources'))
        self.assertContains(
            response,
            "StreamWebs offers a number of resources to get you started in " +
            "the field")
        self.client.logout()

    def test_reg_user_has_upload_perm(self):
        """Reg user that has upload perm can also access the upload page"""
        self.assertTrue(self.special_user.has_perm(
            'streamwebs.can_upload_resources'))
        self.assertFalse(self.special_user.has_perms(
            ['streamwebs.can_promote_users', 'streamwebs.can_view_stats']))
        self.assertFalse(
            self.special_user.groups.filter(name='admin').exists())
        self.client.login(username='special_user', password='specialpassword')
        response = self.client.get(reverse('streamwebs:resources-upload'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'streamwebs/resources/resources_upload.html')
        self.assertContains(response, 'Upload a new resource')

        """Should also be able to view link in resources.html"""
        response = self.client.get(reverse('streamwebs:resources'))
        self.assertContains(
            response,
            "StreamWebs offers a number of resources to get you started in " +
            "the field")

        self.client.logout()

    def test_reg_user_without_upload_perm(self):
        """Reg user without upload perm should be denied access to the page"""
        self.assertFalse(self.reg_user.has_perms(
            ['streamwebs.can_promote_users', 'streamwebs.can_view_stats',
             'streamwebs.can_upload_resources']))
        self.assertFalse(
            self.reg_user.groups.filter(name='admin').exists())
        self.client.login(username='reg_user', password='regpassword')
        response = self.client.get(reverse('streamwebs:resources-upload'))
        self.assertRaises(PermissionDenied)
        self.assertEquals(response.status_code, 403)
        self.assertTemplateNotUsed(
            response, 'streamwebs/resources/resources_upload.html')

        """Should not be able to view link in resources.html"""
        response = self.client.get(reverse('streamwebs:resources'))
        self.assertContains(
            response,
            "StreamWebs offers a number of resources to get you started in " +
            "the field")
        self.assertNotContains(response, "Upload a new resource")

        self.client.logout()

    def test_view_with_bad_blank_data(self):
        """If user submits bad (blank) form, form errors displayed"""
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('streamwebs:resources-upload'), {})
        self.assertFormError(response, 'res_form', 'name',
                             'This field is required.')
        self.assertFormError(response, 'res_form', 'res_type',
                             'This field is required.')
        self.assertFormError(response, 'res_form', 'sort_order',
                             'This field is required.')
        self.client.logout()

    def test_data_sheet_resource_upload(self):
        self.client.login(username='admin', password='adminpassword')

        response = self.client.post(reverse('streamwebs:resources-upload'), {
            'name': 'New Sheet Type',
            'res_type': 'data_sheet',
            'downloadable': self.temp_file,
            'thumbnail': self.temp_img,
            'sort_order': 1000,
            }
        )
        self.assertRedirects(
            response,
            (reverse('streamwebs:resources-data-sheets')),
            status_code=302,
            target_status_code=200)
        self.assertTrue(Resource.objects.filter(name='New Sheet Type').filter(
            res_type='data_sheet').filter(sort_order=1000).exists())
        self.client.logout()

    def test_publication_resource_upload(self):
        self.client.login(username='special_user', password='specialpassword')

        response = self.client.post(reverse('streamwebs:resources-upload'), {
            'name': 'New Publication',
            'res_type': 'publication',
            'downloadable': self.temp_file,
            'thumbnail': self.temp_img,
            'sort_order': 0,
            }
        )
        self.assertRedirects(
            response,
            (reverse('streamwebs:resources-publications')),
            status_code=302,
            target_status_code=200)
        self.assertTrue(Resource.objects.filter(name='New Publication').filter(
            res_type='publication').filter(sort_order=0).exists())
        self.client.logout()
