# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-08 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamwebs', '0029_auto_20171108_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='ripaquaticsurvey',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Field notes'),
        ),
        migrations.AddField(
            model_name='soil_survey',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Field notes'),
        ),
    ]
