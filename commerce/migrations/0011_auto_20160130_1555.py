# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0010_asset_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
