# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 10:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlockPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('color', models.CharField(max_length=255, verbose_name='Цвет')),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('left', models.IntegerField()),
                ('top', models.IntegerField()),
                ('role', models.CharField(max_length=255, verbose_name='Роль')),
                ('creator', models.CharField(max_length=255, verbose_name='Создатель')),
            ],
        ),
        migrations.CreateModel(
            name='Canvas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_width', models.IntegerField(verbose_name='Ширина ячейки')),
                ('cell_height', models.IntegerField(verbose_name='Длина ячейки')),
                ('strip_count', models.IntegerField(verbose_name='Количество столбцов')),
                ('row_count', models.IntegerField(verbose_name='Количество рядов')),
            ],
        ),
        migrations.CreateModel(
            name='ContentBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Текст')),
                ('id_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='number.BlockPage', verbose_name='Блок контента')),
            ],
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('date', models.DateField(verbose_name='Дата создания')),
            ],
        ),
        migrations.CreateModel(
            name='NumDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата выхода номера')),
                ('short_num', models.IntegerField(verbose_name='Порядковый номер в году')),
                ('full_num', models.IntegerField(verbose_name='Общий порядковый номер')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Название')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('deleted', models.IntegerField()),
                ('order_init', models.IntegerField()),
                ('id_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='number.Number', verbose_name='Номер')),
            ],
        ),
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Название рубрики')),
            ],
        ),
        migrations.CreateModel(
            name='TaskBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_topic', models.CharField(max_length=255, verbose_name='Топик')),
                ('task_description', models.CharField(max_length=255, verbose_name='Описание')),
                ('task_author', models.CharField(max_length=255, verbose_name='Автор')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='rubric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='number.Rubric', verbose_name='Газетная рубрика'),
        ),
        migrations.AddField(
            model_name='blockpage',
            name='content_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='number.ContentBlock'),
        ),
        migrations.AddField(
            model_name='blockpage',
            name='id_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='number.Page', verbose_name='Страница блока'),
        ),
        migrations.AddField(
            model_name='blockpage',
            name='task_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='number.TaskBlock'),
        ),
    ]
