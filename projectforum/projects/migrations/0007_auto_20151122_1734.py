# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20151122_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message=b'Please enter a positive amount')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(max_length=2048),
        ),
    ]
