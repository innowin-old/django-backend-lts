# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-18 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='c_type',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='related_instance_id',
        ),
        migrations.AddField(
            model_name='hashtag',
            name='hashtag_base',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='base_hashtags', to='base.Base'),
            preserve_default=False,
        ),
    ]