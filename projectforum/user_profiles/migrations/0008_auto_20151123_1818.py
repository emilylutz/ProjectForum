# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0007_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='averageRating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='showRatings',
            field=models.BooleanField(default=False, verbose_name=b'Publicly show ratings'),
        ),
    ]
