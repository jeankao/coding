# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-19 04:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0045_enroll_score_memo_django'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='memo_c',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='work',
            name='memo_e',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='work',
            name='publish',
            field=models.BooleanField(default=False),
        ),
    ]
