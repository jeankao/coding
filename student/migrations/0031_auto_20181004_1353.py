# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-04 05:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0030_auto_20181004_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='science1question',
            old_name='twork_id',
            new_name='work_id',
        ),
    ]