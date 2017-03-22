from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import *

def Main(request):
    return HttpResponse('12')






def Auth(request):
    login = request.POST['login']
    password = request.POST['password']
    query = Users.objects.filter(login=login,password=password).values('login','password','role','rubric')
    print(query)
    mass = []
    for a in query:
        mass.append(a['rubric'])


    if query:
        request.session['login'] = query[0]['login']
        request.session['password'] = query[0]['password']
        request.session['role'] = query[0]['role']
        request.session['rubric_passible'] = mass
        Users.objects.filter(login=login).update(auth=False)

        return redirect('/number/')
    else:
        return HttpResponse('неверный логин или пароль')
