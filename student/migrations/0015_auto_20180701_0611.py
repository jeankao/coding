# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-06-30 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_auto_20180701_0057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enroll',
            name='group_show',
        ),
        migrations.AddField(
            model_name='enroll',
            name='groupshow',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
