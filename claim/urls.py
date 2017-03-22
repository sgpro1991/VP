from django.conf.urls import url
from claim.views import *

urlpatterns = (
    url(r'^$', Main),
    url(r'^auth/$',Auth),
    url(r'^check_auth/$',CheckAuth),
    url(r'^exit/$',Exit),
    url(r'^create_task/$',CreateTask),
    url(r'^my_task/$',MyTask),
    url(r'^delete_task/$',DeleteTask),
    url(r'^get_param_task/$',GetInfoTask),
    url(r'^edit_param_task/$', EditParamTask),
    url(r'^change_date/$', ChangeDate),
    #url(r'^check_cookie/$', CheckCookie2),
    url(r'^check_bitrix_account/$', CheckBitrixAccount),
    url(r'^create_bitrix_account/$', CreateBitrixAccount),
    url(r'^faq/$', FaqQuestion),


)
