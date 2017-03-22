from django.contrib import admin

# Register your models here.

from .models import *


class PageInline(admin.TabularInline):
    model = Page
    #extra = 3


class NumberAdmin(admin.ModelAdmin):
    inlines = [PageInline]
    list_display = ['id','date', 'title']


class PageAdmin(admin.ModelAdmin):
    list_display = ['id','date','rubric']
    list_filter = ['rubric','deleted']
    pass


class RubricAdmin(admin.ModelAdmin):
    list_display = ['title','sortir']
    ordering = ['sortir','title']
    list_editable = ['sortir']



class CanvasAdmin(admin.ModelAdmin):
    list_display = ['strip_count','row_count']



class NumDateAdmin(admin.ModelAdmin):
    list_display = ['date','short_num', 'full_num']
    pass


class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ['id']
    pass


class BlockPageAdmin(admin.ModelAdmin):
    list_display = ['id']
    pass


admin.site.register(NumDate,NumDateAdmin)


admin.site.register(Page,PageAdmin)
admin.site.register(Rubric,RubricAdmin)
admin.site.register(Canvas,CanvasAdmin)
admin.site.register(TaskBlock)



admin.site.register(Number,NumberAdmin)
admin.site.register(BlockPage,BlockPageAdmin)
admin.site.register(ContentBlock,ContentBlockAdmin)
