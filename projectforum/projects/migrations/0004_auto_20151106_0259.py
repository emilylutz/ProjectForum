# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20151102_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='applicants',
            field=models.ManyToManyField(related_name='projects_applied_to', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='team_members',
            field=models.ManyToManyField(related_name='current_projects', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
