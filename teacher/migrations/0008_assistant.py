# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-08-19 03:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_auto_20180708_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
            ],
        ),
    ]