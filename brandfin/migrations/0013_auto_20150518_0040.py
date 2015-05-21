# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brandfin', '0012_reporttemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttemplate',
            name='description',
            field=models.CharField(help_text=b'Template description', max_length=100),
        ),
        migrations.AlterField(
            model_name='reporttemplate',
            name='title',
            field=models.CharField(help_text=b'Template title', max_length=100),
        ),
    ]
