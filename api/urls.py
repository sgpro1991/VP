from django.conf.urls import url
from api.views import *

urlpatterns = (
    url(r'^get_pages/$', GetPages),
    url(r'^exit/',Exit),
    url(r'^get_rubrics/', GetRubrics),
    url(r'^get_block_stats/', get_block_stats),
    url(r'^get_content/$',GetContent),
    url(r'^list_task/$',ListTask),
)
