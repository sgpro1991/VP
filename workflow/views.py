from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from users.models import *
from claim.models import Task
from channels.handler import AsgiHandler
from channels.channel import Group




import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi
from plan.wsgi import application as plan



class MyAppWebSocket(tornado.websocket.WebSocketHandler):
    # Simple Websocket echo handler. This could be extended to
    # use Redis PubSub to broadcast updates to clients.

    clients = set()

    def open(self):
        # logging.info('Client connected')
        MyAppWebSocket.clients.add(self)


    def on_message(self, message):
        # logging.log('Received message')
        MyAppWebSocket.broadcast(message)
        print(message)

    def on_close(self):
        # logging.info('Client disconnected')
        if self in MyAppWebSocket.clients:
            MyAppWebSocket.clients.remove(self)

    @classmethod
    def broadcast(cls, message):
        for client in cls.clients:
            client.write_message(message)










def test(request):
    MyAppWebSocket
    return render(request,'test.html')







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







def Main(request):

    try:
        if request.COOKIES['uid']:
            login = True
    except:
            login = False

    return render(request,'index-doc.html',{'login':login})



def CrateDoc(request):
    if Auth(request) == True:
        id_task = request.GET.get('id',False)

        if id_task:
            task = Task.objects.get(id=id_task)

            return HttpResponse(task.description)



    else:
        return HttpResponse(status=403)
