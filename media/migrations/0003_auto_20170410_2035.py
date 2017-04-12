# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 20:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_media_identity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='uploader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medias', to=settings.AUTH_USER_MODEL),
        ),
    ]
