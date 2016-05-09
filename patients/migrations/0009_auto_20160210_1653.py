# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 16:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0008_auto_20160201_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurement',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterField(
            model_name='measurement',
            name='patientMeasurement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='patients.PatientMeasurement'),
        ),
        migrations.AlterField(
            model_name='measurementtimelineevent',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 2, 10, 16, 53, 35, 364787)),
        ),
        migrations.AlterField(
            model_name='patientmeasurement',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patientMeasurements', to='patients.MeasurementCategory'),
        ),
        migrations.AlterField(
            model_name='patientmeasurement',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patientMeasurements', to='patients.Patient'),
        ),
        migrations.AlterUniqueTogether(
            name='patientmeasurement',
            unique_together=set([('patient', 'category')]),
        ),
    ]