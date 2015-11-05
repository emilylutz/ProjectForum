# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userreview',
            old_name='test',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='userreview',
            old_name='rating',
            new_name='score',
        ),
    ]
