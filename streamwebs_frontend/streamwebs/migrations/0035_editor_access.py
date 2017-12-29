# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 11:28
from __future__ import unicode_literals

from django.db import migrations, models

def give_editor_access(apps, schema_editor):
    Users = apps.get_model("auth", "User")
    Group = apps.get_model('auth', 'Group')

    org_contributor, created = Group.objects.get_or_create(name='org_author')
    org_editor, created = Group.objects.get_or_create(name='org_admin')

    for user in Users.objects.all():
        # Strip away contributor permission if they had it
        if user.groups.filter(name='org_author').exists():
            user.groups.remove(org_contributor)
        # Add editor permission
        user.groups.add(org_editor)
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('streamwebs', '0034_macro_totals'),
    ]

    operations = [
        migrations.RunPython(give_editor_access)
    ]