from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
# Create your views here.

from django.conf import settings


from users.models import Users
from .models import Number,Page,Rubric,Canvas,BlockPage,NumDate
from scheduler.models import Scheduler, ScheduledPage

from django.core.exceptions import ObjectDoesNotExist

from dateutil.rrule import rrulestr
from datetime import datetime, date, time
import uuid
import recurrence
from users.logger import Logger  as log




def Test(request):
    from django.core.mail import send_mail
    send_mail(
        'Subject here',
        'Here is the message.',
        'bitrix_vp@oblgazeta.ru',
        ['fwd1db8j7ex8iu8ccw8cc44400co@oblgazeta.bitrix24.ru'],
        fail_silently=False,
    )
    return HttpResponse(1)




def Auth(request):
    try:
        if request.COOKIES['uid'] and request.COOKIES['AUTH_SSID']:
            param = Users.objects.filter(login = request.COOKIES['uid']).values('login','role','rubric','auth')
            #print('=====================================')
            mass = []

            for a in param:
                mass.append(a['rubric'])
                triger = a['auth']
                request.session['role'] = a['role']


            request.session['rubric_passible'] = mass

            #print(request.session['rubric_passible'],request.session['role'] )
            #print(triger)
            #print('=====================================')

            if triger == True:
                param.update(auth=False)
                return False
            else:
                return True
    except:
        return False











"""
def Main(request):
    if not Auth(request):
        return render(request,'form_enter.html')


    try:
        all_numbers = Number.objects.filter(date__gte=date.today()).order_by('-id').values('id','title','date')

        query = Number.objects.filter(id=request.GET['id']).values('id','title')
        request.session['id'] = query[0]['id']

        pass_rubric = Rubric.objects.filter(pk__in=request.session['rubric_passible']).values('title')

        request.session['number_title'] = query[0]['title']

        query  = Rubric.objects.all()
        return render(request,'index2.html',{'pass_rubric':pass_rubric,'rubric':query,'id_number':request.session['id'],'all_numbers':all_numbers})

    except:

        all_numbers = Number.objects.all().order_by('-date').values('id','title','date')

        query  = Rubric.objects.all()
        return render(request,'index2.html',{'pass_rubric':'','rubric':query,'id_number':'','all_numbers':all_numbers})
"""


def Main(request):
    if Auth(request) == True:
        pass
    else:
        return redirect('/block/delete_ssid/')

    #return HttpResponse(status=200)
    #if not Auth(request):
    #    return render(request,'form_enter.html')
    all_numbers = Number.objects.filter(date__gte=date.today()).order_by('date').values('id','title','date')
    #all_numbers = Number.objects.filter(date__gte=date.today()).order_by('date')[:10].values('id','title','date')
    rubrics  = Rubric.objects.all()
    try:
        if request.session['rubric_passible']:
            pass_rubric = Rubric.objects.filter(pk__in=request.session['rubric_passible']).values('title')
        else:
            pass_rubric = ''
    except:
        pass_rubric = ''

    try:
        if request.COOKIES['uid']:
            login = True
    except:
            login = False


    if request.GET.get('id', False):
        query = Number.objects.filter(id=request.GET['id']).values('id','title')
        request.session['id'] = query[0]['id']
        request.session['number_title'] = query[0]['title']
    else:
        request.session['id'] = ''
        request.session['number_title'] = ''

    return render(request, 'index2.html', {
        'version':settings.STATIC_VERSION,
        'pass_rubric': pass_rubric,
        'rubric': rubrics,
        'id_number': request.session['id'],
        'all_numbers': all_numbers,
        'login':login
    })





def Login(request):
    return redirect('/block/delete_ssid/')











def CreateNumber(request):

    try:
        date_string = datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse(status=400)

    try:
        number = Number.objects.get(date=date_string)

    except ObjectDoesNotExist:

        if not Auth(request) or int(request.session['role']) < 4:
            return HttpResponse(status=403)

        request.session['number_title'] = request.GET.get('number_title')
        number = Number(title = request.GET.get('number_title'),date=date_string)
        number.save()

        log(request.COOKIES['uid'],13,'Создал номер на '+str(date_string))

        add_scheduled_pages_to_number(request,number)

    request.session['id'] = number.id

    return HttpResponse(number.id)






def GetSession(request):
    if Auth(request) == True:
        pass
    else:
        return HttpResponse(status=500)

    try:
        return HttpResponse(request.session['number_title'])
    except:
        return HttpResponse('')





def GetNumberId(request):
    if Auth(request) == True:
        pass
    else:
        return HttpResponse(status=500)

    try:
        return HttpResponse(request.session['id'])
    except:
        return HttpResponse('')







# add page to number
def add_page(request,num, page_title, rubric, order):
    """
    num - "Number" object
    page_title - string
    rubric - "Rubric" object
    order - integer
    """

    insert_page = Page(
        id_number=num,
        title=page_title,
        rubric=rubric,
        deleted=0,
        order_init=order
    )
    insert_page.save()
    log(request.COOKIES['uid'],4,'Создал полосу с рубрикой "'+str(rubric)+'" порядок страницы '+str(order))
    return insert_page



def add_scheduled_blocks_to_page(num, created_page):
    scheduler = Scheduler.objects.all()
    for a in scheduler:
        d = a.recurrences.after(datetime(num.date.year, num.date.month, num.date.day))
        if d:
            if num.date == d.date():
                if created_page.rubric.title in a.rubrics.split(","):
                    ins = BlockPage(
                        id_page=created_page,
                        color=a.color,
                        title=a.title,
                        width=a.width,
                        height=a.height,
                        left=a.left,
                        top=a.top,
                        role=a.role,
                        creator=a.creator
                    )
                    ins.save()
                    #print(ins)


def add_scheduled_pages_to_number(request,num):
    scheduledpages = ScheduledPage.objects.all()
    for page in scheduledpages:
        next_scheduled_date = page.recurrences.after(datetime(num.date.year, num.date.month, num.date.day))
        if next_scheduled_date:
            if num.date == next_scheduled_date.date():
                created_page = add_page(request,num, page.rubric.title, page.rubric, page.order_init)
                add_scheduled_blocks_to_page(num, created_page)















def CreatePage(request):
    ####################################################################
    if not Auth(request) or int(request.session['role']) < 4:
        return HttpResponse(status=500)

    ####################################################################

    #page_title = request.GET.get('page_title', False)
    #print('type(page_title)')
    #print(type(page_title))
    rubric = Rubric.objects.get(pk=request.GET['rubric'])
    order = request.GET['order']
    num = Number.objects.get(pk=request.GET['id'])
    #print('def CreatePage(request):')
    #print(page_title)
    created_page = add_page(request,num, rubric.title, rubric, order)
    request.session['page_id'] = created_page.id

    add_scheduled_blocks_to_page(num, created_page)

    return HttpResponse(request.session['page_id'])










def Pages(request):
    if Auth(request) == True:
        pass
    else:
        return HttpResponse(status=500)

    if request.session['number_title'] != '':
        query = request.session['number_title']
    else:
        query = ''

    return render(request,'pages.html',{'session':query})









def DeletePage(request):
    if Auth(request) == True:
        pass
    else:
        return HttpResponse(status=500)


    if int(request.session['role']) >= 4:
        pass
    else:
        return HttpResponse(status=500)

    try:
        b = Page.objects.filter(id=request.GET['id']).values('id_number','rubric')
        a = Page.objects.filter(id=request.GET['id']).update(deleted=1)
        log(request.COOKIES['uid'],6, 'id полосы '+str(request.GET['id'])+' находилась в номере id '+str(b[0]['id_number']))
        return HttpResponse(b[0]['id_number'])
    except:
        return HttpResponse(status=500)












def NumberView(request):
    if Auth(request) == True:
        pass
    else:
        return redirect('/block/delete_ssid/')

    try:
        pages = Page.objects.filter(id_number=request.GET['id'], deleted=0).order_by('order_init')
        number = Number.objects.get(id=request.GET['id'])
        canvas = Canvas.objects.all().values('cell_width','cell_height','strip_count','row_count')[:1]
        numdate = NumDate.objects.filter(date=number.date)[:1]
    except:
        return HttpResponse('такого номера нет')


    try:
        if request.COOKIES['uid']:
            login = True
    except:
            login = False

    if numdate:
        numdate = numdate[0]
    else:
        numdate = None

    return render_to_response('number.html', {'rubrics_all':Rubric.objects.all().order_by('sortir','title'),
                                            'pages': pages,
                                            'version':settings.STATIC_VERSION,
                                            'canvas': canvas, 'number': number,
                                            'numdate': numdate,'login':login,
                                            'date_number':number.date})












def NumberView2(request):
    if Auth(request) == True:
        pass
    else:
        return redirect('/block/delete_ssid/')

    query = Page.objects.filter(id_number=request.GET['id'],deleted=0).values('id','title','rubric').order_by('order_init')
    print(query)
    return render(request,'number2.html')
