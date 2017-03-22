from django.conf.urls import url
from scheduler.views import *

urlpatterns = (
    url(r'^$', Main),
    url(r'^add/$', Add),
)
