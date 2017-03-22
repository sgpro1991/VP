from django.shortcuts import render, render_to_response, get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
# Create your views here.

####################################################################################
#from blocks import bitrix_bot as bot
####################################################################################
from django.core.mail import send_mail

from django.conf import settings
from users.models import Users,Logging
from .models import Blocks
from number.models import BlockPage, ContentBlock, Canvas, Page, Rubric, Number, TaskBlock

from claim.models import Task,Bitrix
#import requests
from django import forms
from scheduler.models import Scheduler

from plan import configuration as config

import json
from django.core.exceptions import ObjectDoesNotExist
from users.logger import Logger  as log


def Auth(request):
    try:
        if request.COOKIES['uid'] and request.COOKIES['AUTH_SSID']: #and request.session['role']:
            param = Users.objects.filter(login = request.COOKIES['uid']).values('login','role','rubric','auth')
            print('=====================================')
            mass = []

            for a in param:
                mass.append(a['rubric'])
                triger = a['auth']
                request.session['role'] = a['role']


            request.session['rubric_passible'] = mass

            print(request.session['rubric_passible'],request.session['role'] )
            print(triger)
            print('=====================================')

            if triger == True:  #yXzFwIyk

                post_data = {'ssid': request.COOKIES['AUTH_SSID']}
                resp = requests.post('http://auth.oblgazeta.ru/api/1.0/?logout', data=post_data)
                content = resp.content





                response = HttpResponse('http://auth.oblgazeta.ru/login.php?redirect=%s' % request.build_absolute_uri('/'))
                #response.delete_cookie('AUTH_SSID')
                response.set_cookie('AUTH_SSID', domain=".oblgazeta.ru", max_age=0)
                response.set_cookie('uid', domain=".oblgazeta.ru", max_age=0)
                param.update(auth=False)
                return False
            else:
                return True
    except:
        return False







def DeleteSsid(request):
        print(request.build_absolute_uri('/'))
        #print(request.GET)
        #response = HttpResponseRedirect('http://auth.oblgazeta.ru/login.php?redirect=http://vp.oblgazeta.ru/number/')
        response = HttpResponseRedirect('http://auth.oblgazeta.ru/login.php?redirect=%s' % request.build_absolute_uri('/number/'))
        #response.delete_cookie('AUTH_SSID')
        response.set_cookie('AUTH_SSID', domain=".oblgazeta.ru", max_age=0)
        response.set_cookie('uid', domain=".oblgazeta.ru", max_age=0)
        try:
            response.delete_cookie('check')
        except:
            pass

        return response






def CheckRole(request):
    if Auth(request) == False:
        return HttpResponse(status=403)

    if request.GET.get('arg',False) != False:
        if request.GET['arg'] == '1':
            response = HttpResponse('1')
            response.set_cookie('check', '1')
            print('lalal')
            return response

        if request.GET['arg'] == '2':
            response = HttpResponse('2')
            response.set_cookie('check', '1', max_age=0)
            print('nonono')
            return response
    else:
         print('bababab')




    try:
        if request.COOKIES['check']:
            return HttpResponse('1')
    except:
        return HttpResponse('2')





def CheckRule(request):
    return HttpResponse(request.session['role'])








class CourseForm(forms.ModelForm):
   class Meta:
      model = Scheduler
      fields = ('recurrences',)




#################################
# РЕНДЕР СТРАНИЦЫ РЕДАКТИРОВАНИЯ
#################################

def main(request):

    if Auth(request) == False:
        return redirect('/block/delete_ssid/')
    try:
        if request.COOKIES['uid']:
            login = True
        else:
            login = False
    except:
        login = False




    current_page = get_object_or_404(Page.objects, id=request.GET['id'])
    rubric = current_page.rubric

    if rubric.id not in request.session['rubric_passible']:
        return HttpResponse('У вас недостаточно прав на эту полосу')

    request.session['page_id'] = request.GET['id']
    page_blocks = current_page.blockpage_set.all()


    return render_to_response('by_id.html', {
        'id_number': current_page.id_number,
        'rubrics': Rubric.objects.all(),
        'form': CourseForm,
        'rubric': rubric.title,
        'id_page': current_page.id,
        'order': current_page.order_init,
        'date_number': current_page.id_number.date,
        'canvas': Canvas.objects.last(),
        'page_blocks': page_blocks,
        'complete':current_page.complete,
        'login':login,
        'version':settings.STATIC_VERSION,
        'rubrics_all':Rubric.objects.all().order_by('sortir','title'),
        #'basket_blocks': Blocks.objects.all(),
        'basket_blocks': Blocks.objects.filter(show_in_basket=True),
    })











####################################
#  ОПОВЕЩЕНИЕ ЕБУЧИЙ БИТРИКС
####################################
def BITRIX(id):
    task  = Task.objects.get(id=id)
    try:
        uid_bitrix = Bitrix.objects.get(creator = task.creator)
        message = "Утверждена ваша задача \n "+task.title+" \n"+task.description
        uid = uid_bitrix.bitrix_uid
        send_mail('Оповещение из визуального планирования:', message, config.DEFAULT_FROM_EMAIL,
            [uid], fail_silently=False)
    except:
        return 0









def EndPage(request):
    page = Page.objects.get(pk=request.GET['id'])
    page.complete = int(request.GET.get('value'))
    page.save()

    number = page.id_number
    print(number.id)

    # check all pages in number
    pages = Page.objects.filter(id_number=number,complete=False,deleted=0)
    pages_in_number = Page.objects.filter(id_number=number)
    if pages:
        # deapprove number
        number.complete = False
        number.save()
    else:
        # complete number
        number.complete = True
        number.save()
        log(request.COOKIES['uid'],12,' номер '+str(number))
        print('---------------------------------------')
        pages_id = []
        for page in pages_in_number:
            pages_id.append(page.id)

        blocks = BlockPage.objects.filter(id_page__in=pages_id)
        tasks = []
        for a in blocks:
            if a.task_id is not None:
                tasks.append(a.task_id)
        for b in tasks:
            Task.objects.filter(id=b.id).update(status=20)
            BITRIX(b.id)
        print('---------------------------------------')
        #bot.Prt('Номер на '+str(page.date.date())+' запланирован подробнее: \nhttp://vp.oblgazeta.ru/number/number_view/?id='+str(number.id)+'&resolutions=100')


    return HttpResponse('1')






'''
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
    task_id = models.ForeignKey('TaskBlock', blank=True, null=True, on_delete=models.SET_NULL)
    creator = models.CharField('Создатель',max_length=255)
    content_id = models.ForeignKey('ContentBlock', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):              # __unicode__ on Python 2
        return "%s -> %s -> %s" % (self.id_page.id_number.title, self.id_page.order_init, self.id)
'''



def AddBlockAllView(request):
    if not Auth(request):
        return redirect('/block/delete_ssid/')

    if int(request.session['role']) < 4:
        return HttpResponse(status=500)

    id_page = Page.objects.get(pk=request.GET['id'])


    print(request.GET['color'])
    add_block = BlockPage.objects.create(id_page=id_page,title="",color='#'+request.GET['color'],width=280,height=210,left=0,top=55,role=request.session['role'],creator=request.COOKIES['uid'])
    add_block.save()
    return HttpResponse(add_block.id)
    #return HttpResponse(request.GET['color'])











###############################
# ПОМЕНЯТЬ РУБРИКУ
###############################
def ChangeRubric(request):
    Auth(request)
    if int(request.session['role']) < 4:
        return HttpResponse(status=500)

    page = Page.objects.get(pk=request.GET['id_page'])
    log(request.COOKIES['uid'],5,' Поменял рубрику с "'+str(page.rubric)+'" на "'+str(request.GET['value'])+'"')
    page.rubric = Rubric.objects.get(title=request.GET['value'])
    page.save()


    return HttpResponse('1')




###################################
# ПОМЕНЯТЬ БЛОКИ НА ОБЩЕМ ВИДЕ
##################################
def ChangePosition(request):
    if int(request.session['role']) < 4:
        return HttpResponse(status=500)

    left = int(request.GET['left'])
    top = int(request.GET['top'])
    if request.GET['param'] == '1':

        block_update = BlockPage.objects.filter(pk=request.GET['id'])
        #print(block_update)
        one = BlockPage.objects.get(pk=request.GET['id'])


        block_update.update(id_page=request.GET['page'])
        block_update.update(left=left,top=top)

        for a in block_update:
            two = str(request.GET['page'])

        log(request.COOKIES['uid'],2,'Блок id='+request.GET['id']+' на общем виде сменил плосу с id='+str(one.id_page.id)+' на id='+two)
        return HttpResponse(request.GET['left']+'||||'+request.GET['id']+'|||'+request.GET['page'])
    else:
        current_pos = BlockPage.objects.get(pk=request.GET['id'])
        block_update = BlockPage.objects.filter(pk=request.GET['id']).update(left=left,top=top)
        log(request.COOKIES['uid'],2,'На общем виде  на текущей полосе c id='+str(current_pos.id_page)+', Блок c id='+str(current_pos.id)+' сменил позицию  с left:'+str(current_pos.left)+' top:'+str(current_pos.top)+' на left:'+str(left)+' top:'+str(top))

        print(block_update)
        return HttpResponse('2')






######################################
# ПОМЕНЯТЬ ДЛИНУ И ШИРИНУ
######################################
def ChangeParametrs(request):
    if not Auth(request):
        return HttpResponse(status=403)

    #if int(request.session['role']) < 4:
    #    return HttpResponse(status=403)
    print(request.session['role'])
    change_param = BlockPage.objects.get(pk=request.GET['id'])#.update(width=request.GET['width'],height=request.GET['height'])
    if request.session['role'] == change_param.role:
        BlockPage.objects.filter(pk=request.GET['id']).update(width=request.GET['width'],height=request.GET['height'])
        log(request.COOKIES['uid'],2,'Смена длины и ширины блока id='+str(change_param.id)+' с width:'+str(change_param.width)+' height:'+str(change_param.height)+' на width:'+str(request.GET['width'])+' height:'+str(request.GET['height']))

        return HttpResponse(status=200)
    elif int(request.session['role'])>3:
        BlockPage.objects.filter(pk=request.GET['id']).update(width=request.GET['width'],height=request.GET['height'])
        log(request.COOKIES['uid'],2,'Смена длины и ширины блока id='+str(change_param.id)+' с width:'+str(change_param.width)+' height:'+str(change_param.height)+' на width:'+str(request.GET['width'])+' height:'+str(request.GET['height']))

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)





###############################
# ПОМЕНЯТЬ ПОРЯДОК
###############################
def ChangeOrder(request):
    if int(request.session['role']) >= 4:
        pass
    else:
        return HttpResponse(status=500)

    Page.objects.filter(id=request.GET['id_page']).update(order_init=request.GET['value'])
    return HttpResponse(status=200)



def CheckAdminSwich(request):
    if Auth(request) == False:
            return redirect('/number/login/')
    try:
        if int(request.session['role']) >= 4:
            log(request.COOKIES['uid'],14,'Режим администратора')
            return HttpResponse(1)
        else:
            return HttpResponse(0)
    except:
        return HttpResponse(0)






#################################
# GET BLOCKS API
#################################
def GetBlocks(request):
    json1 = []
    #blocks = BlockPage.objects.get(id_page_id=request.GET['id'])
    blocks = BlockPage.objects.filter(id_page=request.GET['id'])

    for a in blocks:

        if a.content_id != None or a.content_id == '':
            content = 1
        else:
            content = ''

        """
        print('-------')
        print(a.task_id)
        if a.task_id:
            task = a.task_id.title
        else:
            task = ''
        print('-------')
        """
        print('-------')
        print(a.title)
        print('-------')
        json1.append({
            'id_page': a.id_page.id,
            'id_block': a.id,
            'title': a.title,
            'color': a.color,
            'width': a.width,
            'height': a.height,
            'left': a.left,
            'top': a.top,
            'task': a.task_id.title if a.task_id else '',
            'author': a.task_id.name if a.task_id else '',
            'task_description':a.task_id.description if a.task_id else '',
            'content': str(content)
        })

    print(json1)

    return HttpResponse(json.dumps(json1, ensure_ascii=False), content_type="application/json; charset=utf-8")
    '''
    return HttpResponse('1')
    '''
























@csrf_exempt
def CreateUpdateBlocks(request):

    width = request.POST['width'][:-2]
    height = request.POST['height'][:-2]
    left = request.POST['left'][:-2]
    top = request.POST['top'][:-2]
    id = request.POST.get('id', False);
    title = request.POST['title']
    color = request.POST['color']

    if id:
        current_block = BlockPage.objects.get(pk=id)
        log_current_block_top = current_block.top
        log_current_block_left = current_block.left
        if int(request.session['role']) >= int(current_block.role):
            current_block.color = color
            current_block.title = title
            current_block.width = width
            current_block.height = height
            current_block.left = left
            current_block.top = top
            current_block.role = request.session['role']
            current_block.save()
            log(request.COOKIES['uid'],2,'Смена позиции блока id='+str(id)+'\n c \n top:'+str(log_current_block_top)+' \n left:'+str(log_current_block_left)+' \n на \n top:'+str(top)+'\n left:'+str(left))
        else:
           return HttpResponse(status=403)

    else:
        current_page = Page.objects.get(pk=request.session['page_id'])
        insert = BlockPage(
            id_page=current_page,
            color=color,
            title=title,
            width=width,
            height=height,
            left=left,
            top=top,
            role=request.session['role'],
            creator=request.COOKIES['uid']
        )
        insert.save()

        id = insert.pk
        log(request.COOKIES['uid'],1,'Создал блок с id='+str(id))



    #return HttpResponse(request.POST['id'])
    return HttpResponse(id)


















def GetBlockParam(request):
    #try:
        block = BlockPage.objects.get(pk=request.GET.get('id'))
        #print(block.title)
        json1 = [{
            'id_page': block.id_page.id,
            'title': block.title,
            'color': block.color,
            'width': block.width,
            'height': block.height,
            'role':request.session['role'],
            'task': block.task_id.id if block.task_id else None
        }]

        return HttpResponse(json.dumps(json1, ensure_ascii=False), content_type="application/json; charset=utf-8")
    #except:
    #    return HttpResponse(status=404)







def DeleteBlock(request):
    if not Auth(request):
        return HttpResponse(status=403)

    if 'id' not in request.GET:
        return HttpResponse(status=404)

    block = BlockPage.objects.get(pk=request.GET.get('id'))

    if int(request.session['role']) < int(block.role):
        return HttpResponse(status=403)

    if block.delete():
        log(request.COOKIES['uid'],3,' id='+str(request.GET.get('id')))
        return HttpResponse('ok')
    else:
        return HttpResponse('error')







@csrf_exempt
def EditParamBlock(request):

    try:

        if int(request.session['role']) > 3:
            BlockPage.objects.filter(pk=request.POST.get('id')).update(
                title=request.POST['title'],
                color=request.POST['color'],
                width=request.POST['width'],
                height=request.POST['height']
            )
        else:
            BlockPage.objects.filter(pk=request.POST.get('id')).update(
                color=request.POST['color'],
                width=request.POST['width'],
                height=request.POST['height']
            )
        #log(request.COOKIES['uid'],2,' id='+str(request.POST.get('id'))+'\n title: '+str(request.POST['title'])+'\n color: '+str(request.POST['color'])+'\n width: '+str(request.POST['width'])+'\n height: '+str(request.POST['height']))
        return HttpResponse(status=202)
    except:
        return HttpResponse(status=404)

























@csrf_exempt
def CreateBlock(request):
    try:
        a = Blocks(title=request.POST['title'],width=request.POST['w'],height=request.POST['h'],color=request.POST['c'])
        a.save()

        return HttpResponse('1')
    except:
        return HttpResponse('2')





###########################
# ADD TASK
###########################
@csrf_exempt
def AddTask(request):
    if not Auth(request):
        return HttpResponse(status=500)

    task = BlockPage.objects.get(pk=request.POST['id'])
    print(task.task_id)
    # HTTP 502 if block already has a task.
    if task.task_id:
        return HttpResponse(status=502)
    else:
        task = Task.objects.get(id=int(request.POST['task_id']))
        if task.status == 0: # если задача НЕ закреплена за блоком
            current_block = BlockPage.objects.filter(pk=request.POST['id']).update(task_id=int(request.POST['task_id']))
            Task.objects.filter(id=int(request.POST['task_id'])).update(status=10)
            log(request.COOKIES['uid'],15,'Прикрепил задачу с id='+str(request.POST['task_id'])+' к блоку id='+str(request.POST['id']))
            return HttpResponse(status=200)
        else:
            return HttpResponse(content=task.id,status=403)




@csrf_exempt
def RedirectTask(request):
    if not Auth(request):
        return HttpResponse(status=500)

    current_block = BlockPage.objects.filter(task_id=request.POST['task_id']).update(task_id='')
    update_block = BlockPage.objects.filter(pk=request.POST['id']).update(task_id=int(request.POST['task_id']))
    return HttpResponse(status=200)



    '''
    insert = TaskBlock(
        task_topic=request.POST['topic'],
        task_description=request.POST['description'],
        task_author=request.POST['author']
    )
    insert.save()

    current_block.task_id = insert
    current_block.save()

    json1 = [{
        'task_topic': request.POST['topic'],
        'task_description': request.POST['description'],
        'task_author': request.POST['author'],
    }]

    return HttpResponse(json.dumps(json1, ensure_ascii=False), content_type="application/json; charset=utf-8")
    '''
    #return HttpResponse(insert.task_author)
    #return HttpResponse(status=200)






###########################
# CHECK TASK
###########################
def CheckTask(request):
    ### checks if block has assigned task
    # return task_id.id or empty string

    try:
        current_block = BlockPage.objects.get(pk=request.GET['id'])
        if current_block.task_id:
            return HttpResponse(current_block.task_id.pk)
        else:
            return HttpResponse('')
    except ObjectDoesNotExist:
        return HttpResponse('')








def GetOneTask(request):
    # gets info about one task from django db
    # request.GET['id'] = task id from django db

    task = Task.objects.get(pk=request.GET['id'])

    json1 = [{
        'task_topic': task.title,
        'task_description': task.description,
        'task_author': task.name,
    }]

    return HttpResponse(json.dumps(json1, ensure_ascii=False), content_type="application/json; charset=utf-8")







def DeleteOneTask(request):
    BlockPage.objects.filter(id=request.GET.get('id')).update(task_id='')
    Task.objects.filter(id=request.GET.get('id_task')).update(status=0)
    log(request.COOKIES['uid'],16,'task id='+str(request.GET.get('id_task'))+' block id='+str(request.GET.get('id')))
    return HttpResponse('1')














#ContentBlock
@csrf_exempt
def SetData(request):
    current_block = BlockPage.objects.get(pk=request.POST['id'])
    creator = current_block.creator

    if creator != request.COOKIES['uid']:
        print(current_block.role,request.session['role'])
        if request.session['role'] < current_block.role:
            return HttpResponse(status=403)

    if request.POST['param'] == 'insert':
        try:
            prov = ContentBlock.objects.filter(id_block=request.POST['id'])
            print(prov)
            if prov:
                prov.update(content=request.POST['content'])
                #prov.save()

                return HttpResponse(prov.id)

            else:
                query = ContentBlock(
                    id_block_id=request.POST['id'],
                    content=request.POST['content']
                )
                query.save()
                BlockPage.objects.filter(pk=request.POST['id']).update(content_id=query.id)
                #current_block.update(content_id=query.id)
                #current_block.content_id = query
                #current_block.save()
                #print(query.id)
                return HttpResponse(query.id)


        except:
            return HttpResponse(status=203)


    if request.POST['param'] == 'put':
        try:
            query = ContentBlock.objects.filter(id_block=request.POST['id']).values('content')

            return HttpResponse(query[0]['content'])
        except:
            return HttpResponse('')
