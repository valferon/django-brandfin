# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brandfin', '0010_auto_20150504_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='daily_run',
            field=models.BooleanField(default=False, help_text=b'Schedule query to run daily'),
        ),
    ]
