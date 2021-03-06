# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 18:27
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0007_auto_20160131_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementTimelineEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(default=datetime.datetime(2016, 2, 1, 13, 27, 20, 224786))),
                ('notes', models.TextField(blank=True)),
                ('owner', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patientMeasurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timelineEvent', to='patients.PatientMeasurement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='measurementcategory',
            name='typicalMax',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='measurementcategory',
            name='typicalMin',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
