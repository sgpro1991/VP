# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('number', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
