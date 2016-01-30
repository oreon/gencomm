# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 15:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0003_auto_20160130_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpPatient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(blank=True, max_length=30)),
                ('lastName', models.CharField(blank=True, max_length=30)),
                ('user', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exppt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
