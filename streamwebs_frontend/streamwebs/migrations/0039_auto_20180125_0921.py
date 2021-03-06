# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-25 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('streamwebs', '0038_galleryalbum_galleryfile_galleryimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='galleryalbum',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='galleryalbum',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='galleryfile',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='galleryfile',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=250, verbose_name='title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=250, verbose_name='title'),
            preserve_default=False,
        ),
    ]
