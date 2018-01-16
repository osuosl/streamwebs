# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-16 13:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('streamwebs', '0037_approve_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='streamwebs.School', verbose_name='school')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='streamwebs.Site', verbose_name='Stream/Site name')),
            ],
            options={
                'verbose_name': 'gallery album',
                'verbose_name_plural': 'gallery albums',
            },
        ),
        migrations.CreateModel(
            name='GalleryFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_file', models.FileField(null=True, upload_to='gallery_files/', verbose_name='file')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date and time')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='streamwebs.School', verbose_name='school')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='streamwebs.Site', verbose_name='Stream/Site name')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'gallery file',
                'verbose_name_plural': 'gallery files',
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='gallery_images/', verbose_name='image')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date and time')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streamwebs.GalleryAlbum', verbose_name='album')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='streamwebs.School', verbose_name='school')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='streamwebs.Site', verbose_name='Stream/Site name')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'gallery image',
                'verbose_name_plural': 'gallery images',
            },
        ),
    ]
