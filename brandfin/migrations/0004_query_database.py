# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0003_dataconnection_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='database',
            field=models.ForeignKey(default='', blank=True, to='brandfin.DataConnection'),
            preserve_default=False,
        ),
    ]
