# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0004_auto_20151025_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='skills',
            field=models.ManyToManyField(related_name='user_profiles', to='user_profiles.UserSkillTag', blank=True),
        ),
    ]
