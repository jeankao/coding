# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-28 03:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0024_sfcontent_sfreply_sfwork'),
    ]

    operations = [
        migrations.CreateModel(
            name='Science1Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_id', models.IntegerField(default=0)),
                ('types', models.IntegerField(default=0)),
                ('text', models.TextField(default='')),
                ('pic', models.FileField(blank=True, null=True, upload_to=b'')),
                ('picname', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Science1Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(default=0)),
                ('index', models.IntegerField(default=0)),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='work',
            name='score',
            field=models.IntegerField(default=-2),
        ),
    ]
