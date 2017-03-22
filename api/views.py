from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse


from number.models import Page, Rubric, Canvas, ContentBlock, BlockPage
# Create your views here.
from claim.models import Task

import json

from datetime import datetime


def GetPages(request):
    #try:
    query = Page.objects.filter(id_number=request.GET['id'],deleted=0).values('id','title','rubric','order_init').order_by('order_init')
    mass = []

    for a in query:
        mass.append({
            'id':a['id'],
            'title':a['title'],
            'rubric':a['rubric'],
            'order_init':a['order_init'],
            'complete':a['complete']
        })

    #return JsonResponse(mass)
    return HttpResponse(json.dumps(mass, ensure_ascii=False), content_type="application/json; charset=utf-8")
    #except:
        #return HttpResponse(status=404)



def GetRubrics(request):
    mass = []

    rubrics = Rubric.objects.all().values('id','title')

    for a in rubrics:
        mass.append({
            'id':a['id'],
            'title':a['title'],

        })

    return HttpResponse(json.dumps(mass, ensure_ascii=False), content_type="application/json; charset=utf-8")




def Exit(request):

    #del request.session['login']
    #del request.session['password']
    #del request.session['role']
    #del request.session['rubric_passible']
    return redirect('/block/delete_ssid')





def GetContent(request):
    try:
        block = BlockPage.objects.get(pk=request.GET.get('id'))
        content = block.content_id.content

        return HttpResponse(content)
    except:
        return HttpResponse(status=404)








#################################################


#def square_by_px(block_width_px, block_height_px):
def square_by_px(request):
    # example: {% ad_square_by_px 100 200 %}

    cell_width = 43.125
    cell_height = 21.167
    horizontal_distance = 5
    vertical_distance = 3.528
    canvas = Canvas.objects.last()
    cell_width_px = canvas.cell_width
    cell_height_px = canvas.cell_height

    block_width_px, block_height_px = request.GET.get('block_width_px', False), request.GET.get('block_height_px', False)
    block_width_px = int(block_width_px)
    block_height_px = int(block_height_px)

    if not (block_width_px and block_height_px):
        return HttpResponse(status=501)

    def ad_square(columns, rows):
        # example: {% ad_square 1 2 %}

        total_width = cell_width * columns + horizontal_distance * (columns - 1)
        total_height = cell_height * rows + vertical_distance * (rows - 1)
        square = total_width * total_height / 100

        return ("%.2f" % square)

    def newspaper_maxchars(block_width_px, block_height_px):

        cell_width = 43.125
        cell_height = 21.167
        vertical_distance = 3.528
        columns = block_width_px / cell_width_px
        rows = block_height_px / cell_height_px

        maxchars = block_height_px * 26 * (block_width_px / cell_width_px) / vertical_distance
        return int(maxchars)


    columns = block_width_px / cell_width_px
    rows = block_height_px / cell_height_px

    return_dict = {
        'square': ad_square(columns, rows),
        'maxchars': newspaper_maxchars(block_width_px, block_height_px),
    }
    return HttpResponse(json.dumps(return_dict, ensure_ascii=False), content_type="application/json; charset=utf-8")


def get_block_stats(request):

    columns, rows = request.GET.get('columns', False), request.GET.get('rows', False)
    columns = int(columns)
    rows = int(rows)

    if not (columns and rows):
        return HttpResponse(status=501)

    cell_width = 43.125
    cell_height = 21.167
    horizontal_distance = 5
    vertical_distance = 3.528

    total_width = cell_width * columns + horizontal_distance * (columns - 1)
    total_height = cell_height * rows + vertical_distance * (rows - 1)
    square = total_width * total_height / 100
    square = ("%.2f" % square)

    maxchars = int(cell_height * rows * 26 * columns / vertical_distance)

    return_dict = {
        'square': square,
        'maxchars': maxchars,
    }
    return HttpResponse(json.dumps(return_dict, ensure_ascii=False), content_type="application/json; charset=utf-8")


#################################################





def ListTask(request):
    d_f = request.GET['from'].split('.')
    d_t = request.GET['to'].split('.')

    from_date = datetime.date(datetime.strptime(str(d_f[2]+'-'+d_f[1]+'-'+d_f[0]),'%Y-%m-%d'))
    to_date = datetime.date(datetime.strptime(str(d_t[2]+'-'+d_t[1]+'-'+d_t[0]),'%Y-%m-%d'))


    #output_json = []
    import pprint
    import collections
    pp = pprint.PrettyPrinter(indent=4)
    out_dict = collections.OrderedDict()

    tasks = Task.objects.filter(date__range=[from_date, to_date]).order_by('date')

    for task in tasks:

        task_date_str = task.date.strftime('%d.%m.%Y')

        if task_date_str not in out_dict:
            out_dict[task_date_str] = []
            print(out_dict)
        out_dict[task_date_str].append(
            {
                'id': task.id,
                'title': task.title,
                'creator': task.creator,
                'name': task.name,
                'description': task.description,
                'alias_dep': task.alias_dep,
                'deportament': task.deportament,
                'count_chars': task.count_chars
            }
        )
    #out_dict = collections.OrderedDict(sorted(out_dict.items()))
    pp.pprint(out_dict)

    #return JsonResponse(mass)
    #return HttpResponse(json.dumps(mass, ensure_ascii=False), content_type="application/json; charset=utf-8")
    #return HttpResponse(1)
    return HttpResponse(json.dumps(out_dict, ensure_ascii=False), content_type="application/json; charset=utf-8")
