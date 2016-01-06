# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bed',
            name='patient',
            field=models.ForeignKey(null=True, blank=True, to='patients.Patient', related_name='bed'),
        ),
    ]
