# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_auto_20180611_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='helps',
            field=models.IntegerField(default=0, choices=[(0, '\u5168\u90e8\u9760\u81ea\u5df1\u60f3'), (1, '\u540c\u5b78\u5e6b\u4e00\u9ede\u5fd9'), (2, '\u540c\u5b78\u5e6b\u5f88\u591a\u5fd9'), (3, '\u89e3\u7b54\u5e6b\u4e00\u9ede\u5fd9'), (4, '\u89e3\u7b54\u5e6b\u5f88\u591a\u5fd9'), (5, '\u8001\u5e2b\u5e6b\u4e00\u9ede\u5fd9'), (6, '\u8001\u5e2b\u5e6b\u5f88\u591a\u5fd9')]),
        ),
    ]
