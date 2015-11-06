# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20151102_0249'),
        ('ratings', '0005_auto_20151105_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreview',
            name='project',
            field=models.ForeignKey(default=None, to='projects.Project'),
            preserve_default=False,
        ),
    ]
