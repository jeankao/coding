# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-15 11:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0051_auto_20190319_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantLight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(default=0)),
                ('light', models.FloatField(default=0)),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]