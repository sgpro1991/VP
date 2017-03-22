from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import *
from number.models import BlockPage

def Main(request):
    return HttpResponse(status=200)


@csrf_exempt
def Add(request):

    rubrics  = ",".join(request.POST.getlist('scheduler_rubric'))

    period = request.POST['recurrences']
    block = BlockPage.objects.filter(pk=request.POST['scheduler_id_block']).values('title','color','width','height','left','top','role','creator')


    print(rubrics)
    insert = Scheduler(
        title=block[0]['title'],
        color=block[0]['color'],
        width=block[0]['width'],
        height=block[0]['height'],
        left=block[0]['left'],
        top=block[0]['top'],
        role=block[0]['role'],
        creator=block[0]['creator'],
        recurrences=period,
        rubrics=rubrics
    )
    insert.save()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
