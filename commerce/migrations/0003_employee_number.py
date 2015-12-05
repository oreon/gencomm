# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_auto_20151026_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='number',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
