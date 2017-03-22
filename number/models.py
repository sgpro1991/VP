from django.db import models
from django.forms import ModelForm
# Create your models here.
from claim.models import Task


class Number(models.Model):
    title = models.CharField('Название' ,max_length=255)
    date = models.DateField('Дата создания')
    complete = models.BooleanField(default=False)
    def __str__(self):              # __unicode__ on Python 2
        return self.title


class Rubric(models.Model):
    title = models.CharField('Название рубрики', max_length=255, unique=True)
    alias = models.CharField('Название рубрики алиас', max_length=255, null=True, blank=True)
    sortir = models.IntegerField('Группировка', null=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.title


class Page(models.Model):
    id_number = models.ForeignKey(Number, verbose_name=u'Номер')
    title = models.CharField('Название', max_length=255, blank=True)
    rubric = models.ForeignKey(Rubric, verbose_name=u'Газетная рубрика')
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    deleted = models.IntegerField()
    order_init = models.IntegerField()
    complete = models.BooleanField(default=False)
    def __str__(self):              # __unicode__ on Python 2
        #return "%s -> %s" % (self.id_number, self.order_init)
        return "%s -> %s" % (self.id_number.date, self.order_init)


class BlockPage(models.Model):
    id_page = models.ForeignKey(Page, verbose_name=u'Страница блока')
    #id_block = models.CharField('Идентификатор' ,max_length=255)
    title = models.CharField('Название' ,max_length=255)
    color = models.CharField('Цвет' ,max_length=255)
    width = models.IntegerField()
    height = models.IntegerField()
    left = models.IntegerField()
    top = models.IntegerField()
    role = models.CharField('Роль',max_length=255)
    #task_id = models.ForeignKey('TaskBlock', blank=True, null=True, on_delete=models.SET_NULL)
    task_id = models.ForeignKey(Task, blank=True, null=True, on_delete=models.SET_NULL)
    creator = models.CharField('Создатель',max_length=255)
    content_id = models.ForeignKey('ContentBlock', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):              # __unicode__ on Python 2
        return "%s -> %s -> %s" % (self.id_page.id_number.title, self.id_page.order_init, self.id)


class ContentBlock(models.Model):
    #id_block = models.CharField('Идентификатор' ,max_length=255)
    id_block = models.ForeignKey(BlockPage, verbose_name=u'Блок контента')
    content = models.TextField('Текст')
    def __str__(self):              # __unicode__ on Python 2
        #return self.id_block
        return self.id_block.title


class TaskBlock(models.Model):
    #id_block = models.CharField('Идентификатор' ,max_length=255)
    #id_block = models.ForeignKey(BlockPage, verbose_name=u'Идентификатор блока')
    task_topic = models.CharField('Топик' ,max_length=255)
    task_description = models.CharField('Описание' ,max_length=255)
    task_author = models.CharField('Автор' ,max_length=255)
    def __str__(self):              # __unicode__ on Python 2
        return self.task_topic


class Canvas(models.Model):
    cell_width = models.IntegerField('Ширина ячейки')
    cell_height = models.IntegerField('Длина ячейки')
    strip_count = models.IntegerField('Количество столбцов')
    row_count = models.IntegerField('Количество рядов')


class NumDate(models.Model):
    date = models.DateField('Дата выхода номера')
    short_num = models.IntegerField('Порядковый номер в году')
    full_num = models.IntegerField('Общий порядковый номер')
    #def __str__(self):              # __unicode__ on Python 2
    #    return self.date
    class Meta:
        ordering = ['-date']
