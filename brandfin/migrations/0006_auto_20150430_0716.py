# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0005_remove_query_database'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataconnection',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Can only have one dataconnection active'),
        ),
        migrations.AddField(
            model_name='schema',
            name='source',
            field=models.ForeignKey(to='brandfin.DataConnection'),
        ),
    ]
