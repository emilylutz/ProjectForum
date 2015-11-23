# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20151115_0508'),
        ('user_profiles', '0005_auto_20151025_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bookmarked_projects',
            field=models.ManyToManyField(to='projects.Project', blank=True),
        ),
    ]
