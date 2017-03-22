from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Task)




class BitrixAdmin(admin.ModelAdmin):
    search_fields = [ 'creator' ]
    list_display = [ 'creator']


admin.site.register(Bitrix,BitrixAdmin)


class FaqAdmin(admin.ModelAdmin):
    search_fields = ( 'title','text' )
    list_display = [ 'title']


admin.site.register(Faq,FaqAdmin)
