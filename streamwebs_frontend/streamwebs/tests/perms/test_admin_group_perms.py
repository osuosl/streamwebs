from django.test import TestCase
from django.contrib.auth.models import Group, Permission


class AdminGroupPermissionsTestCase(TestCase):
    def setUp(self):
        self.admin, self.created = Group.objects.get_or_create(name='admin')
        self.expected_perms = {
            'can upload resources',
            'can promote other users',
            'can view site statistics',
        }

    def test_admin_group_already_exists(self):
        admin, created = Group.objects.get_or_create(name='admin')
        self.assertFalse(created)
        self.assertEqual(admin.name, 'admin')

    def test_perms_already_exist(self):
        upload, created = Permission.objects.get_or_create(
            name='can upload resources')
        self.assertTrue(upload)
        self.assertFalse(created)

        promote, created = Permission.objects.get_or_create(
            name='can promote other users')
        self.assertTrue(promote)
        self.assertFalse(created)

        stats, created = Permission.objects.get_or_create(
            name='can view site statistics')
        self.assertTrue(stats)
        self.assertFalse(created)

    def test_admin_group_has_approp_perms(self):
        admin_perms = self.admin.permissions.all()
        for admin_perm in admin_perms:
            self.assertIn(admin_perm.name, self.expected_perms)

        self.assertEqual(len(self.expected_perms), len(admin_perms))
