# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-05 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0036_science2json'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Science2Data',
        ),
        migrations.DeleteModel(
            name='Science2Expression',
        ),
        migrations.DeleteModel(
            name='Science2Flow',
        ),
    ]
