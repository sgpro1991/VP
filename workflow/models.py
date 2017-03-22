from django.db import models
from claim.models import Task
from number.models import Number






class Document(models.Model):
    task_id = models.ForeignKey(Task, blank=True, null=True)
    name = models.CharField('Имя создателя',max_length=255)
    login = models.CharField('Логин создателя', max_length=255)
    owner = models.CharField('Владелец', max_length=255, null=True, blank=True)

    title = models.CharField('Заголовок', max_length=255)
    sub_title = models.CharField('подзаголовок', max_length=255)
    text = models.TextField('Текст')

    date_create = models.DateTimeField('Дата время создания')
    status = models.CharField('Статус',max_length=255)
    number = models.ForeignKey(Number, blank=True, null=True)
    strip = models.CharField('Полоса', max_length=255, blank=True, null=True)

    newspaper = models.BooleanField('Для газеты')
    site = models.BooleanField('Для сайта')

    deleted = models.BooleanField('Удален',default=False)
