# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0007_auto_20151130_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expereince', models.IntegerField(default=1)),
                ('customerOrder', models.ForeignKey(to='commerce.Employee', related_name='employeeSkills')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='employeeskill',
            name='product',
            field=models.ForeignKey(to='commerce.Skill'),
        ),
    ]
