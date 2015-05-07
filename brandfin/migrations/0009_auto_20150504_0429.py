# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0008_auto_20150504_0149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='result_data',
        ),
        migrations.RemoveField(
            model_name='query',
            name='result_headers',
        ),
        migrations.AddField(
            model_name='query',
            name='result',
            field=models.TextField(null=True, blank=True),
        ),
    ]
