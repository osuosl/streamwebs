# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-30 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamwebs', '0026_soil_survey_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='ripaquaticsurvey',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Field notes'),
        ),
    ]
