# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-09 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_identity'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='identity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='identity_medias', to='users.Identity'),
            preserve_default=False,
        ),
    ]
