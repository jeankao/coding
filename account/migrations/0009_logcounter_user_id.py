# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-04-20 02:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_daycounter_lessoncounter_logcounter'),
    ]

    operations = [
        migrations.AddField(
            model_name='logcounter',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
