from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_migrate


@receiver(post_migrate)
def init_groups_and_perms(sender, **kwargs):

    content_type, created = ContentType.objects.get_or_create(
        app_label='streamwebs', model='unused')

    # These are the new security groups

    # Create the OrgAuthor permission and group
    is_org_author, created = Permission.objects.get_or_create(
        codename='is_org_author', name='Org Author Permission',
        content_type=content_type
    )
    org_author, created = Group.objects.get_or_create(name='org_author')
    if created:
        org_author.permissions.add(is_org_author)

    # Create the OrgAdmin permission and group
    is_org_admin, created = Permission.objects.get_or_create(
        codename='is_org_admin', name='Org Admin Permission',
        content_type=content_type
    )
    org_admin, created = Group.objects.get_or_create(name='org_admin')
    if created:
        org_admin.permissions.add(is_org_admin, is_org_author)

    # Create the SuperAdmin permission and group
    is_super_admin, created = Permission.objects.get_or_create(
        codename='is_super_admin', name='Super Admin Permission',
        content_type=content_type
    )
    super_admin, created = Group.objects.get_or_create(name='super_admin')
    if created:
        super_admin.permissions.add(
                                   is_super_admin, is_org_admin, is_org_author)

    # These are the old security groups
    # can_upload, created = Permission.objects.get_or_create(
    #     codename='can_upload_resources', name='can upload resources',
    #     content_type=content_type)

    # can_promote, created = Permission.objects.get_or_create(
    #     codename='can_promote_users', name='can promote other users',
    #     content_type=content_type)

    # can_view_stats, created = Permission.objects.get_or_create(
    #     codename='can_view_stats', name='can view site statistics',
    #     content_type=content_type)

    # admin, created = Group.objects.get_or_create(name='admin')
    # if created:
    #     admin.permissions.add(can_upload, can_view_stats)
    #     print("admin group created; permissions added")
