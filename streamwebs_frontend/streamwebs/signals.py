from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_migrate


@receiver(post_migrate)
def init_groups_and_perms(sender, **kwargs):
    content_type, created = ContentType.objects.get_or_create(
        app_label='streamwebs', model='unused')

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
