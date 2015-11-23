# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_auto_20151115_0508'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=2048)),
                ('applicant', models.ForeignKey(related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'project application',
                'verbose_name_plural': 'project applications',
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='applicants',
        ),
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
        migrations.AddField(
            model_name='projectapplication',
            name='project',
            field=models.ForeignKey(related_name='applications', to='projects.Project'),
        ),
    ]
