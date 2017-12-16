# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-16 12:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_customer_organization'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['-pk'], 'verbose_name_plural': 'Basics'},
        ),
        migrations.AddField(
            model_name='organization',
            name='created_time',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='updated_time',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now),
        ),
    ]
