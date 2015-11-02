# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_auto_20151022_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='applicants',
            field=models.ManyToManyField(related_name='projects_applied_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='team_members',
            field=models.ManyToManyField(related_name='current_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'Accepting Applicants'), (2, b'In progress'), (3, b'Canceled'), (4, b'Finished')]),
        ),
    ]
