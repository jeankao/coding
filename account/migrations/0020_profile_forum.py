# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-15 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_profile_lock6'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='forum',
            field=models.IntegerField(default=0),
        ),
    ]
