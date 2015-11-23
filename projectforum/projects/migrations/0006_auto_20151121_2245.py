# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20151115_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='project',
            name='payment',
            field=models.IntegerField(choices=[(1, b'Lump Sum'), (2, b'Hourly')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'Accepting Applicants'), (2, b'In Progress'), (3, b'Canceled'), (4, b'Finished')]),
        ),
    ]
