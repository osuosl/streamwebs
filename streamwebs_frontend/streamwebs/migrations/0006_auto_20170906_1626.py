# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-06 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamwebs', '0005_merge_20170906_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soil_survey',
            name='distance',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='distance from stream'),
        ),
    ]
