# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-07-01 03:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0002_showgroup_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='showreview',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
