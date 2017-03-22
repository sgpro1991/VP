from django.db import models
from recurrence.fields import RecurrenceField
# Create your models here.
from number.models import Rubric



# Автоматически создаваемые блоки внутри страниц
class Scheduler(models.Model):
    title = models.CharField('Название' ,max_length=255)
    color = models.CharField('Цвет' ,max_length=255)
    width = models.IntegerField()
    height = models.IntegerField()
    left = models.IntegerField()
    top = models.IntegerField()
    role = models.CharField('Роль',max_length=255)
    creator = models.CharField('Создатель',max_length=255)
    recurrences = RecurrenceField('Периодичность')
    rubrics = models.TextField('Рубрики')


# Автоматически создаваемые страницы при создании номера
class ScheduledPage(models.Model):
    description = models.CharField('Описание', max_length=255, default=None) # чисто описание в админке
    recurrences = RecurrenceField('Периодичность')
    rubric = models.ForeignKey(Rubric, null=True, verbose_name='Газетная рубрика')
    order_init = models.IntegerField(verbose_name='Номер страницы')
