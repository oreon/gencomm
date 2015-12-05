# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('gender', models.CharField(max_length=30, blank=True)),
                ('dob', models.DateField(blank=True)),
                ('firstName', models.CharField(max_length=30, blank=True)),
                ('lastName', models.CharField(max_length=30, blank=True)),
                ('department', models.ForeignKey(to='commerce.Department', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
