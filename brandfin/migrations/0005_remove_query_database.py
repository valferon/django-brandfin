# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0004_query_database'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='database',
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reportName', models.CharField(help_text=b'Report Name', max_length=300)),
                ('lastRefresh', models.DateTimeField(auto_now=True)),
                ('reportData', models.TextField(null=True, blank=True)),
                ('originQuery', models.ForeignKey(to='brandfin.Query')),
            ],
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('schemaName', models.CharField(help_text=b'Schema Name', max_length=300)),
                ('lastRefresh', models.DateTimeField(auto_now=True)),
                ('schemaData', models.TextField(null=True, blank=True)),
            ],
        )
    ]

