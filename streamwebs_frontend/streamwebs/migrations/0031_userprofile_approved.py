# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamwebs', '0030_auto_20171108_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
