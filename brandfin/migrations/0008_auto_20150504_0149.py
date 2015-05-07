# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0007_auto_20150501_0512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='result',
            new_name='result_data',
        ),
        migrations.RemoveField(
            model_name='query',
            name='lastRefresh',
        ),
        migrations.AddField(
            model_name='query',
            name='result_headers',
            field=models.TextField(null=True, blank=True),
        ),
    ]
