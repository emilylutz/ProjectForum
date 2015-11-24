# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0003_auto_20151022_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSkillTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skill', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'user skill tag',
                'verbose_name_plural': 'user skill tags',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='linkedin',
            field=models.URLField(verbose_name=b'Linkedin url', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='openToEmploy',
            field=models.BooleanField(default=False, verbose_name=b'Open to full time employment'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='personal',
            field=models.URLField(verbose_name=b'Personal url', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='showPastProjects',
            field=models.BooleanField(default=False, verbose_name=b'Publicly show past projects'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='showRatings',
            field=models.BooleanField(default=False, verbose_name=b'Public show ratings'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='skills',
            field=models.ManyToManyField(related_name='user_profiles', to='user_profiles.UserSkillTag'),
        ),
    ]
