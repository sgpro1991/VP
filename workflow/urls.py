from django.conf.urls import url
from workflow.views import *

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi
from plan.wsgi import application as plan


urlpatterns = (
    url(r'^$', Main),
    url(r'^create_doc/', CrateDoc),
    url(r'^test/', test),


)
