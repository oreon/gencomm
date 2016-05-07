# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 14:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0010_asset_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0002_auto_20160106_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slot', models.DateTimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='commerce.Employee')),
                ('owner', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateTimeField()),
                ('notes', models.TextField(blank=True)),
                ('owner', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeasurementCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('frequency', models.IntegerField()),
                ('owner', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PatientMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='patients.MeasurementCategory')),
                ('owner', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PatientScheduleProcedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('performDate', models.DateField(blank=True, null=True)),
                ('owner', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('owner', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScheduleProcedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('frequency', models.IntegerField(blank=True)),
                ('owner', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedures', to='patients.Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('U', 'Unknown')], max_length=10)),
                ('owner', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='bedstay',
            name='patient',
        ),
        migrations.AddField(
            model_name='admission',
            name='dischargeDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='admission',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admission', to='patients.Patient'),
        ),
        migrations.AddField(
            model_name='patient',
            name='primaryPhysician',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='commerce.Employee'),
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patientUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='admission',
            name='owner',
            field=models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bed',
            name='owner',
            field=models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bed',
            name='patient',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bed', to='patients.Patient'),
        ),
        migrations.AlterField(
            model_name='bed',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='bedstay',
            name='owner',
            field=models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('U', 'Unknown')], max_length=6),
        ),
        migrations.AlterField(
            model_name='patient',
            name='owner',
            field=models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patient',
            name='state',
            field=django_fsm.FSMField(default='outpatient', editable=False, max_length=50, protected=True),
        ),
        migrations.AddField(
            model_name='profilephoto',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='patients.Patient'),
        ),
        migrations.AddField(
            model_name='patientscheduleprocedure',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduledProcedures', to='patients.Patient'),
        ),
        migrations.AddField(
            model_name='patientscheduleprocedure',
            name='scheduleProcedure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pocedures', to='patients.ScheduleProcedure'),
        ),
        migrations.AddField(
            model_name='patientmeasurement',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='patients.Patient'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='patientMeasurement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measuredValue', to='patients.PatientMeasurement'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='patients.Patient'),
        ),
        migrations.AddField(
            model_name='bed',
            name='ward',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='beds', to='patients.Ward'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='schedules',
            field=models.ManyToManyField(blank=True, related_name='schedules', to='patients.Schedule'),
        ),
        migrations.AlterUniqueTogether(
            name='scheduleprocedure',
            unique_together=set([('schedule', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='patientscheduleprocedure',
            unique_together=set([('scheduleProcedure', 'date', 'patient')]),
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set([('patient', 'slot'), ('doctor', 'slot')]),
        ),
    ]
