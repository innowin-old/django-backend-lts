# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 20:12
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='average',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
    ]