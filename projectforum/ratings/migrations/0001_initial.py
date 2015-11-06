# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20151106_0259'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('comment', models.CharField(max_length=2048)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(to='projects.Project')),
                ('recipient', models.ForeignKey(related_name='reviewed_user', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(related_name='user_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
