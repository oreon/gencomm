# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('state', django_fsm.FSMField(max_length=50, default='free')),
                ('name', models.CharField(max_length=30, blank=True)),
                ('price', models.IntegerField(blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BedStay',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, blank=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField(null=True, blank=True)),
                ('admission', models.ForeignKey(related_name='bedstays', to='patients.Admission')),
                ('bed', models.ForeignKey(related_name='bedstay', to='patients.Bed')),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('U', 'Unknown')], max_length=1, blank=True)),
                ('dob', models.DateField(blank=True)),
                ('firstName', models.CharField(max_length=30, blank=True)),
                ('lastName', models.CharField(max_length=30, blank=True)),
                ('state', django_fsm.FSMField(max_length=50, default='outpatient')),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bedstay',
            name='patient',
            field=models.ForeignKey(related_name='bedstay', to='patients.Patient'),
        ),
        migrations.AddField(
            model_name='bed',
            name='patient',
            field=models.ForeignKey(related_name='bed', to='patients.Patient'),
        ),
    ]
