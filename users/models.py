# -*- coding: utf8 -*-
from django.db import models

# Create your models here.
from number.models import Rubric


class Users(models.Model):
    ROLE_CHOICES = (
        ('5', 'Главный редактор'),
        ('4', 'Секретарь'),
        ('3', 'Начальник полосы'),
        ('2', 'Журналист'),#для таскера
    )
    login = models.CharField('Логин' ,max_length=255,unique=True)
    role = models.CharField('Роль',choices=ROLE_CHOICES,max_length=255)
    rubric = models.ManyToManyField(Rubric, verbose_name='Права на полосы' ,blank=True)
    auth = models.NullBooleanField('Принудительный выход', default=False)
    class Meta:
        verbose_name = 'Пользователи лдап'
        verbose_name_plural = 'Пользователи лдап'

    def __str__(self):              # __unicode__ on Python 2
        return self.login






class Logging(models.Model):
    ITEM_FILTER = (

        ('1', 'СОЗДАНИЕ БЛОКА'),
        ('2', 'РЕДАКТИРОВАНИЕ БЛОКА'),
        ('3', 'УДАЛЕНИЕ БЛОКА'),

        ('4', 'СОЗДАНИЕ ПОЛОСЫ'),
        ('5', 'РЕДАКТИРОВАНИЕ ПОЛОСЫ'),
        ('6', 'УДАЛЕНИЕ ПОЛОСЫ'),

        ('7', 'СОЗДАНИЕ ЗАДАЧИ'),
        ('8', 'РЕДАКТИРОВАНИЕ ЗАДАЧИ'),
        ('9', 'УДАЛЕНИЕ ЗАДАЧИ'),

        ('10', 'ДОБАВЛЕНИЕ ЗАДАЧИ В БЛОК'),
        ('11', 'УДАЛЕНИЕ ЗАДАЧИ ИЗ БЛОКА'),

        ('12', 'ЗАКРЫТИЕ НОМЕРА'),

        ('13', 'СОЗДАНИЕ НОМЕРА'),
        ('14', 'РЕДАКТИРОВАНИЕ НОМЕРА'),

        ('15', 'ПРИКРЕПЛЕНИЕ ЗАДАЧИ В БЛОК'),
        ('16', 'УДАЛЕНИЕ ЗАДАЧИ ИЗ БЛОКА'),

    )

    user = models.CharField('Users', max_length=255)
    message = models.TextField('ПОДРОБНЕЕ' ,max_length=255)
    filter_actions = models.CharField('ДЕЙСТВИЕ', choices=ITEM_FILTER, max_length=255)
    date_time = models.DateTimeField('ДАТА И ВРЕМЯ',auto_now_add=True)
    class Meta:
        verbose_name = 'Логирование'
        verbose_name_plural = 'Логирование'
