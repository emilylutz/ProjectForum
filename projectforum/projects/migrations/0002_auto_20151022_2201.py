# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='amount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(default=10, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='payment',
            field=models.IntegerField(default=1, choices=[(1, b'Lump sum'), (2, b'Hourly')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'In progress'), (2, b'Canceled'), (3, b'Finished')]),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.CharField(max_length=2048, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 23, 5, 1, 23, 345000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
