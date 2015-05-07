# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0002_dataconnection'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataconnection',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
