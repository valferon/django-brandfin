# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0009_auto_20150504_0429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='result',
        ),
        migrations.AddField(
            model_name='query',
            name='result_data',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='query',
            name='result_headers',
            field=models.TextField(null=True, blank=True),
        ),
    ]
