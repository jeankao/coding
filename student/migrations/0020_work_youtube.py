# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-08-18 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0019_auto_20180708_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='youtube',
            field=models.TextField(default=''),
        ),
    ]
