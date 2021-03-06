# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-02 10:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170131_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255, verbose_name='ДЕЙСТВИЕ')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='ДАТА И ВРЕМЯ')),
            ],
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'Пользователи лдап', 'verbose_name_plural': 'Пользователи лдап'},
        ),
        migrations.AddField(
            model_name='logging',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Users'),
        ),
    ]
