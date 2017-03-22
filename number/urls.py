from django.conf.urls import url
from number.views import *

urlpatterns = (
    url(r'^$', Main),
    url(r'^create_number/$',CreateNumber),
    url(r'^get_ses/$',GetSession),
    url(r'^get_id_number/$',GetNumberId),
    url(r'^create_page/$',CreatePage),
    url(r'^pages/$',Pages),
    url(r'^number_view/$',NumberView),
    url(r'^number_view_two/$',NumberView2),
    url(r'^delete_page/$',DeletePage),
    url(r'^login/',Login),
    url(r'^test/',Test),
)
