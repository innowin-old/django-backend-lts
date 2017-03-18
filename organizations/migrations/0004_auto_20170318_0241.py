# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-18 02:41
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20170315_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='business_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None),
        ),
        migrations.AlterField(
            model_name='organization',
            name='correspondence_language',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='picture',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
