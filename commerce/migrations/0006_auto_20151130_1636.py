# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0005_auto_20151028_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='city',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='province',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='street',
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')]),
        ),
    ]
