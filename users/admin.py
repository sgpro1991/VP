from django.contrib import admin
from django.forms import CheckboxSelectMultiple

#import urllib, json
import urllib.request, json

from .models import *
# Register your models here.




def ExitUsers(modeladmin, request, queryset):
    print(queryset)
    for a in queryset:
            Users.objects.filter(pk=a.id).update(auth=True)
    ExitUsers.short_description = 'Принудительный выход'









def SyncLdap(modeladmin, request, queryset):
    #### ПОЛУЧАЕМ JSON С ПОЛЬЗОВАТЕЛЯМИ ИЗ ЛДАПА ########
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    print(data,'-------------------------------------------------->')

    
    ##### БЕРЕМ ВСЕХ ЮЗЕРОВ ИЗ АДМИНКИ ДЖАНГИ И СИНХРОНИЗИРУЕМ РОЛИ С ЛДАПОМ #####
    users = Users.objects.all().only('login','role','id')
    mass = []
    for a in users:
        mass.append(a.login)

        if a.login in data['writer']:
            Users.objects.filter(pk=a.id).update(role=2)

        if a.login in data['manager']:
            Users.objects.filter(pk=a.id).update(role=3)

        if a.login in data['editor']:
            Users.objects.filter(pk=a.id).update(role=4)

        if a.login in data['admin']:
            Users.objects.filter(pk=a.id).update(role=5)


    #### ДОБАВЛЯЕМ НОВЫХ ПОЛЬЗОВАТЕЛЕЙ ЕСЛИ ОНИ ЕСТЬ В АДМИНКИ ДЖАНГИ ######
    mass_ldap=[]
    for param in data:
        if param == 'admin':
            for a in data[param]:
                mass_ldap.append(a)
                if a not in mass:
                    insert = Users(login=a,role=5)
                    insert.save()

        if param == 'editor':
            for a in data[param]:
                mass_ldap.append(a)
                if a not in mass:
                    insert = Users(login=a,role=4)
                    insert.save()

        if param == 'manager':
            for a in data[param]:
                mass_ldap.append(a)
                if a not in mass:
                    insert = Users(login=a,role=3)
                    insert.save()

        if param == 'writer':
            for a in data[param]:
                mass_ldap.append(a)
                print('~~~~~~~~~~~~~~')
                print('a:', a)
                print(mass)
                print('~~~~~~~~~~~~~~')
                if a not in mass:
                    insert = Users(login=a,role=2)
                    insert.save()


    #### УДАЛЯЕМ ЮЗЕРОВ КОТОРЫХ НЕТ В ЛДАПЕ ИЗ ДЖАНГИ ########
    delete_account = list(set(mass)-set(mass_ldap))
    for a in delete_account:
        Users.objects.filter(login=a).delete()

    #SyncLdap.short_description = 'Sync ldap'
    SyncLdap.acts_on_all = True
    SyncLdap.short_description = 'Синхронизация с LDAP'









class UsersAdmin(admin.ModelAdmin):
    list_display = ['id','login','role']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def changelist_view(self, request, extra_context=None):
        try:
            action = self.get_actions(request)[request.POST['action']][0]
            action_acts_on_all = action.acts_on_all
        except (KeyError, AttributeError):
            action_acts_on_all = False

        if action_acts_on_all:
            post = request.POST.copy()
            post.setlist(admin.helpers.ACTION_CHECKBOX_NAME,
                         self.model.objects.values_list('id', flat=True))
            request.POST = post

        return admin.ModelAdmin.changelist_view(self, request, extra_context)



    actions = [ExitUsers,SyncLdap]
    list_filter = ['role']


admin.site.register(Users,UsersAdmin)


class LoggingAdmin(admin.ModelAdmin):
    list_display = ['date_time','user','filter_actions','message']
    list_filter = ['filter_actions']
    search_fields = ['date_time','user','message']

admin.site.register(Logging,LoggingAdmin)
