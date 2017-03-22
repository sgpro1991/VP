from django.db import models

# Create your models here.



class Blocks(models.Model):
    title = models.CharField('Название' ,max_length=255)
    width = models.IntegerField('Ширина, колонок')
    height = models.IntegerField('Высота, модулей')
    color = models.CharField('Цвет',max_length=255)
    show_in_basket = models.BooleanField('Показывать на сайте?', default = True)
    class Meta:
        verbose_name = 'Блок'
        verbose_name_plural = 'Корзина блоков'
