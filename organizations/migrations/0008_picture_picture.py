# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 23:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
        ('organizations', '0007_remove_picture_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='picture',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='media.Media'),
            preserve_default=False,
        ),
    ]