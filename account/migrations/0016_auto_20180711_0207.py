# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-07-10 18:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_message_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='type',
            new_name='message_type',
        ),
    ]
