# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-03 06:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20170203_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logging',
            name='filter_actions',
            field=models.CharField(choices=[('1', 'СОЗДАНИЕ БЛОКА'), ('2', 'РЕДАКТИРОВАНИЕ БЛОКА'), ('3', 'УДАЛЕНИЕ БЛОКА'), ('4', 'СОЗДАНИЕ ПОЛОСЫ'), ('5', 'РЕДАКТИРОВАНИЕ ПОЛОСЫ'), ('6', 'УДАЛЕНИЕ ПОЛОСЫ'), ('7', 'СОЗДАНИЕ ЗАДАЧИ'), ('8', 'РЕДАКТИРОВАНИЕ ЗАДАЧИ'), ('9', 'УДАЛЕНИЕ ЗАДАЧИ'), ('10', 'ДОБАВЛЕНИЕ ЗАДАЧИ В БЛОК'), ('11', 'УДАЛЕНИЕ ЗАДАЧИ ИЗ БЛОКА'), ('12', 'ЗАКРЫТИЕ НОМЕРА'), ('13', 'СОЗДАНИЕ НОМЕРА'), ('14', 'РЕДАКТИРОВАНИЕ НОМЕРА'), ('15', 'ПРИКРЕПЛЕНИЕ ЗАДЧИ В БЛОК'), ('16', 'УДАЛЕНИЕ ЗАДАЧИ ИЗ БЛОКА')], max_length=255, verbose_name='ДЕЙСТВИЕ'),
        ),
    ]
