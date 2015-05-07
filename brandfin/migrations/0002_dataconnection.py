# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('brandfin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name',
                 models.CharField(help_text=b'Name to identify the dataconnection.', unique=True, max_length=255)),
                ('drivername', models.CharField(
                    help_text=b'The name of the database backend. This name will correspond to a module in sqlalchemy/databases or a third party plug-in. Examples: mysql, sqlite',
                    max_length=100)),
                ('username', models.CharField(max_length=300, blank=True)),
                ('password', models.CharField(max_length=300, blank=True)),
                ('host', models.CharField(help_text=b'The name of the host', max_length=300, blank=True)),
                ('port', models.IntegerField(help_text=b'The port number', null=True, blank=True)),
                ('database', models.CharField(help_text=b'The database name', max_length=300)),
            ],
            options={
                'verbose_name_plural': 'Data Connections',
            },
        ),
    ]
