# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0003_employee_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='number',
        ),
    ]
