# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-14 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamwebs', '0010_auto_20170914_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='grasses',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default=0, max_length=250, null=True, verbose_name='grasses'),
        ),
    ]
