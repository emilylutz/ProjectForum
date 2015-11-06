# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0003_auto_20151105_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userreview',
            old_name='user',
            new_name='reviewer',
        ),
    ]
