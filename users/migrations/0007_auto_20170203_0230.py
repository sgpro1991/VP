# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-03 02:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20170202_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logging',
            name='user',
            field=models.CharField(max_length=255, verbose_name='Users'),
        ),
    ]
