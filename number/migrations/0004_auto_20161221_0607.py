# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-21 06:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('number', '0003_number_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockpage',
            name='task_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='claim.Task'),
        ),
    ]
