# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-30 02:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0040_auto_20181230_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='science4work',
            name='publication_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]