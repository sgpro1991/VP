from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.




class Task(models.Model):
    creator = models.CharField('Создатель', max_length=255)
    name = models.CharField('Создатель имя', max_length=255)
    deportament = models.CharField('Отдел', max_length=255)
    alias_dep = models.CharField('Алиас отдела', max_length=255)
    title = models.CharField('Название' ,max_length=255)
    description = models.TextField('Описание')
    date = models.DateField('Дата')
    count_chars = models.IntegerField('Количество символов')
    status = models.IntegerField('Статус заявки', default=0)
    def __str__(self):              # __unicode__ on Python 2
        return str(self.id)



class Bitrix(models.Model):
    creator = models.CharField('Юзер', max_length=255,unique=True)
    bitrix_uid = models.CharField('id битрикса', max_length=255, unique=True)



class Faq(models.Model):
    title = models.CharField('Вопрос', max_length=255)
    text = RichTextUploadingField('Ответ',blank=True, default='')
    def __str__(self):              # __unicode__ on Python 2
        return str(self.title)
