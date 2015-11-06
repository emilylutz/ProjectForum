# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0006_userreview_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userreview',
            name='project',
        ),
    ]
