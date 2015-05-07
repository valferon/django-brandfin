# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0006_auto_20150430_0716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='originQuery',
        ),
        migrations.AddField(
            model_name='query',
            name='lastRefresh',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='query',
            name='result',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]
