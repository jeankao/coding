# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-06-30 23:09
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0015_auto_20180701_0611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enroll',
            name='groupshow',
        ),
        migrations.AddField(
            model_name='enroll',
            name='groups',
            field=models.TextField(default='', validators=[django.core.validators.RegexValidator(regex='^[0-9,]+$')]),
            preserve_default=False,
        ),
    ]