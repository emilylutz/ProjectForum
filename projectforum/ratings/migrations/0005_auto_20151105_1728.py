# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0004_auto_20151105_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreview',
            name='comment',
            field=models.CharField(max_length=2048),
        ),
    ]
