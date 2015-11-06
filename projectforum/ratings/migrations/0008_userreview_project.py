# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20151106_0259'),
        ('ratings', '0007_remove_userreview_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreview',
            name='project',
            field=models.ForeignKey(default=None, to='projects.Project'),
            preserve_default=False,
        ),
    ]
