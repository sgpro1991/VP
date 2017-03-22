from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.core.mail import send_mail

from users.models import Users

from ldap3 import *
import hashlib
import json
import ast
from urllib.parse import unquote
from plan import configuration as config

from .models import Task,Bitrix,Faq
from users.logger import Logger  as log
from number.models import BlockPage,Page




def Main(request):

#    try:
        #if request.COOKIES['AUTH_SSID']:
        if request.COOKIES.get('AUTH_SSID', False):
            print('1')
            try:
                users_dep = Users.objects.get(login = request.COOKIES['uid'])
            except:
                return HttpResponse("Вас нет в Tackep")
            print('11')
            if users_dep.auth == True:
                print('111')
                #response = HttpResponseRedirect('http://auth.oblgazeta.ru/login.php?redirect=http://vp.oblgazeta.ru/claim/')
                response = HttpResponseRedirect('http://auth.oblgazeta.ru/login.php?redirect=%s' % request.build_absolute_uri('/')+'claim')
                print('1111')
                response.set_cookie('AUTH_SSID', domain=".oblgazeta.ru", max_age=0)
                response.set_cookie('uid', domain=".oblgazeta.ru", max_age=0)
                print('11111')
                response.delete_cookie('dep')
                print('111111')
                Users.objects.filter(login = request.COOKIES['uid']).update(auth=False)
                print('2')
                return response

            try:
                if request.COOKIES['dep']:
                    print('3')
                    return render(request,'claim.html')
            except:
                    print('4')
                    dep = []
                    for a in users_dep.rubric.all():
                            dep.append({"cn":a.alias,"ru":a.title})


                    resp = render(request,'claim.html')
                    #resp.set_cookie('login', request.GET['login'])
                    #resp.set_cookie('password', password)
                    resp.set_cookie('dep', json.dumps(dep))
                    return resp
        else:
            print('5')
            return redirect('http://auth.oblgazeta.ru/login.php?redirect=%s' % request.build_absolute_uri('/')+'claim')
#    except:
#        print('6')
#        return redirect('http://auth.oblgazeta.ru/login.php?redirect=http://vp.oblgazeta.ru/claim/')
'''
    try:
        import ast

        name = ast.literal_eval(request.COOKIES['name'])
        #print(name[0]['name'])
    except:
        pass
    return render(request,'claim.html')
'''


def FaqQuestion(request):
    qusetions = Faq.objects.all()
    return render_to_response('faq.html',{'questions':qusetions})



def CheckBitrixAccount(request):
    try:
        uid_bitrix = Bitrix.objects.get(creator = request.COOKIES['uid'])
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=404)




def CreateBitrixAccount(request):
        try:
            message = "Вы успешно указали свои Битрикс24 id"
            uid = request.GET['ac']
            send_mail('Оповещение из визуального планирования:', message, config.DEFAULT_FROM_EMAIL,
                [uid], fail_silently=False)
            insert = Bitrix(creator=request.COOKIES['uid'],bitrix_uid=uid)
            insert.save()
            return HttpResponse(200)
        except:
            return HttpResponse(status=400)





def CheckAuth(request):
    try:
        if request.COOKIES['dep'] and request.COOKIES['AUTH_SSID'] and request.COOKIES['uid']:
            return HttpResponse(request.COOKIES['dep'])
    except:
        return HttpResponse(status=404)








def Auth(request):
    dep = []
    total_entries = 0
    server = Server('192.168.7.180')
    c = Connection(server, user="uid="+request.GET['login']+",ou=people,dc=oblgazeta", password=request.GET['password'])
    if c.bind():

        c.search(search_base = 'ou=plan,ou=services,dc=oblgazeta',
                 search_filter = '(&(cn=*)(memberUid='+request.GET['login']+'))',
                 search_scope = SUBTREE,
                 attributes = ['cn','description']
                )
                 #paged_size = 5)
        total_entries += len(c.response)
        for entry in c.response:
                dep.append({'cn':entry['attributes']['cn'][0],'ru':entry['attributes']['description'][0]})
                print(entry['attributes'])




        #################################################
        c.search(search_base = 'ou=people,dc=oblgazeta',
            search_filter = '(&(objectClass=posixAccount)(uid='+request.GET['login']+'))',
            search_scope = SUBTREE,
            attributes = ['cn']
        )
        name = [{'name':c.response[0]['attributes']['cn'][0]}]
        print(name)
        ################################################





        m = hashlib.md5()
        m.update(request.GET['password'].encode('utf-8'))
        password = m.hexdigest()

        resp = HttpResponse(status=200)
        #resp.set_cookie('login', request.GET['login'])
        #resp.set_cookie('password', password)
        resp.set_cookie('dep', json.dumps(dep))
        resp.set_cookie('name',json.dumps(name))
        return resp
    else:
        return HttpResponse(status=403)





'''

class Task(models.Model):
    creator = models.CharField('Создатель', max_length=255)
    deportament = models.CharField('Отдел', max_length=255)
    alias_dep = models.CharField('Алиас отдела', max_length=255)
    title = models.CharField('Название' ,max_length=255)
    description = models.TextField('Описание')
    date = models.DateField('Дата создания')
    def __str__(self):              # __unicode__ on Python 2
        return self.title
'''



@csrf_exempt
def CreateTask(request):
    try:
        if request.COOKIES['dep'] and request.COOKIES['AUTH_SSID'] and request.COOKIES['uid']:
            pass
    except:
        return HttpResponse(status=403)

    try:
        count = int(request.POST['count'])
    except:
        count = 0

    try:
        #name = ast.literal_eval(request.COOKIES['name']) ####################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        cn = ast.literal_eval(unquote(request.COOKIES['cn']))
        name = cn['name'].replace('+', ' ')
        create_task = Task(creator=request.COOKIES['uid'],
                            name = name,
                            deportament=request.POST['deportament'],
                            alias_dep = request.POST['alias_dep'],
                            title = request.POST['title'],
                            description = request.POST['topic'],
                            date = request.POST['date'],
                            count_chars = count)
        create_task.save()
        log(request.COOKIES['uid'],7,'id='+str(create_task.id))
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=405)



















def MyTask(request):
    try:
        if request.COOKIES['dep'] and request.COOKIES['AUTH_SSID'] and request.COOKIES['uid']:
            pass
    except:
        return HttpResponse(status=403)

    my_tasks = Task.objects.filter(creator=request.COOKIES['uid']).order_by('-id')[int(request.GET['item']):int(request.GET['col'])]

    mass = []

    for a in my_tasks:

        id_page = BlockPage.objects.filter(task_id__id = a.id)

        if id_page:
            la = id_page[0].id_page.id_number.title
            la2 = id_page[0].id_page.id_number.id
        else:
            la = ''
            la2 = ''

        mass.append({
            'id_page':str(la),
            'id_number':str(la2),
            'id':a.id,
            'title':a.title,
            'description':a.description,
            'date':str(a.date),
            'status':a.status,
        })

    #return JsonResponse(mass)
    return HttpResponse(json.dumps(mass, ensure_ascii=False), content_type="application/json; charset=utf-8")







def DeleteTask(request):
    try:
        if request.COOKIES['dep'] and request.COOKIES['AUTH_SSID'] and request.COOKIES['uid']:
            pass
    except:
        return HttpResponse(status=403)

    try:
        task = Task.objects.get(id=request.GET['id'],creator=request.COOKIES['uid'])
        if task.status == 0:
            delete = Task.objects.filter(id=request.GET['id'],creator=request.COOKIES['uid']).delete()
            log(request.COOKIES['uid'],9,'id='+str(request.GET['id']))
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=406)
    except:
        return HttpResponse(status=403)




def GetInfoTask(request):
    try:
        if request.COOKIES['dep'] and request.COOKIES['AUTH_SSID'] and request.COOKIES['uid']:
            pass
    except:
        return HttpResponse(status=403)

    get_task = Task.objects.get(id=request.GET['id'],creator=request.COOKIES['uid'])
    mass = []

    mass.append({
        'id':get_task.id,
        'title':get_task.title,
        'description':get_task.description,
        'date':str(get_task.date),
        'count':get_task.count_chars
    })

    #return JsonResponse(mass)
    return HttpResponse(json.dumps(mass, ensure_ascii=False), content_type="application/json; charset=utf-8")




@csrf_exempt
def EditParamTask(request):
    try:
        task = Task.objects.get(id=request.POST['id'],creator=request.COOKIES['uid'])
        if task.status == 0:
            count = int(request.POST.get('count',False))
            update_task = Task.objects.filter(id=request.POST['id'],creator=request.COOKIES['uid'])
            if count !='':
                update_task.update(title=request.POST['title'],description=request.POST['description'],count_chars=count)
                return HttpResponse(status=200)
            else:
                update_task.update(title=request.POST['title'],description=request.POST['description'],count_chars=0)
                return HttpResponse(status=200)

        else:
            return HttpResponse(status=406)
    except:
        return HttpResponse(status=502)





def ChangeDate(request):
    try:
        task = Task.objects.get(id=request.GET['id'],creator=request.COOKIES['uid'])
        if task.status == 0:
            update_task_date = Task.objects.filter(id=request.GET['id'],creator=request.COOKIES['uid'])
            update_task_date.update(date=request.GET['date'])
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=406)
    except:
        return HttpResponse(status=403)






















def Exit(request):
    response = HttpResponseRedirect('http://auth.oblgazeta.ru/login.php?redirect=%s' % request.build_absolute_uri('/')+'claim')
    response.set_cookie('AUTH_SSID', domain=".oblgazeta.ru", max_age=0)
    response.set_cookie('uid', domain=".oblgazeta.ru", max_age=0)
    response.set_cookie('dep', domain=".oblgazeta.ru", max_age=0)
    Users.objects.filter(login = request.COOKIES['uid']).update(auth=False)
    return response
