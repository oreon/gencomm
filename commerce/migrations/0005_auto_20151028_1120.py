# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0004_remove_employee_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='city',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='province',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='street',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
