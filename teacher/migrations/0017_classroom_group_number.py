# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-01 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0016_auto_20190119_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='group_number',
            field=models.IntegerField(default=8),
        ),
    ]