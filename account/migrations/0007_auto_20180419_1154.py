# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-04-19 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_messagecontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='county',
            name='mapx',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='county',
            name='mapy',
            field=models.IntegerField(default=0),
        ),
    ]
