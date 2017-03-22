from django.contrib import admin

from .models import Scheduler, ScheduledPage

# Register your models here.


class SchedulerAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(Scheduler,SchedulerAdmin)



class ScheduledPageAdmin(admin.ModelAdmin):
    list_display = ['description', 'order_init']
    list_display_links = ['description', 'order_init']
    ordering = ['order_init']
admin.site.register(ScheduledPage, ScheduledPageAdmin)
