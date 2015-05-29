# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brandfin', '0013_auto_20150518_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='weekly_run',
            field=models.BooleanField(default=False, help_text=b'Schedule query to run weekly'),
        ),
    ]
