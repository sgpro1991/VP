from django.contrib import admin


from .models import Blocks
# Register your models here.



class BlocksAdmin(admin.ModelAdmin):
    search_fields = ('title','width','height')
    list_display = [ 'title', 'width','height']




admin.site.register(Blocks,BlocksAdmin)
