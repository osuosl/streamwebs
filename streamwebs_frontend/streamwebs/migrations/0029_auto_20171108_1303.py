# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-08 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamwebs', '0028_auto_20171103_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='bedrock',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='bedrock'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='boulders',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='boulders'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='cobble',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='cobble'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='coniferous_trees',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='coniferous_trees'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='deciduous_trees',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='deciduous_trees'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='ferns',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='ferns'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='grasses',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='grasses'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='gravel',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='gravel'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='large_debris',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='large_debris'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='medium_debris',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='medium_debris'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='sand',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='sand'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='shrubs',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='shrubs'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='silt',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='silt'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='small_debris',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='small_debris'),
        ),
        migrations.AlterField(
            model_name='ripaquaticsurvey',
            name='small_plants',
            field=models.CharField(choices=[('Very Little', 'Very Little'), ('Some', 'Some'), ('A Lot', 'A Lot')], default='Very Little', max_length=250, null=True, verbose_name='small_plants'),
        ),
    ]