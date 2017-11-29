from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_migrate

from streamwebs.models import UserProfile, School


@receiver(post_migrate)
def init_groups_and_perms(sender, **kwargs):

    content_type, created = ContentType.objects.get_or_create(
        app_label='streamwebs', model='unused')

    # These are the new security groups

    is_super_admin, created = Permission.objects.get_or_create(
        codename='is_super_admin', name='Super Admin Permission',
        content_type=content_type
    )

    super_admin, created = Group.objects.get_or_create(name='super_admin')
    if created:
        super_admin.permissions.add(is_super_admin)
        print('super admin group created; permission added')

        sa_account, created = User.objects.get_or_create(
            username='super_admin',
            email='streamwebs@osuosl.org'
        )
        if created:
            sa_account.set_password('super_admin')
            sa_account.save()
            print('SECURITY: superadmin user created')
        else:
            print('SECURITY: superadmin user NOT created')
    

    # These are the old security groups

    can_upload, created = Permission.objects.get_or_create(
        codename='can_upload_resources', name='can upload resources',
        content_type=content_type)

    can_promote, created = Permission.objects.get_or_create(
        codename='can_promote_users', name='can promote other users',
        content_type=content_type)

    can_view_stats, created = Permission.objects.get_or_create(
        codename='can_view_stats', name='can view site statistics',
        content_type=content_type)

    admin, created = Group.objects.get_or_create(name='admin')
    if created:
        admin.permissions.add(can_upload, can_view_stats)
        print("admin group created; permissions added")
