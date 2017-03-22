from django.conf.urls import url
from blocks.views import *



urlpatterns = (

    url(r'^$', main),
    url(r'^create_blocks/$',CreateUpdateBlocks),
    url(r'^remove_block/$', DeleteBlock),
    url(r'^set_data/',SetData),
    url(r'^get_blocks/',GetBlocks),
    url(r'^change_rubric/', ChangeRubric),
    url(r'^add_block/', CreateBlock),
    url(r'^change_order/', ChangeOrder),
    url(r'^add_task/', AddTask),
    url(r'^get_block_param/', GetBlockParam),
    url(r'^edit_block_param/', EditParamBlock),
    url(r'^check_task/', CheckTask),
    url(r'^get_one_task/', GetOneTask),
    url(r'^delete_one_task/', DeleteOneTask),
    url(r'^check_rule/$', CheckRule),
    url(r'^end_page/$',EndPage),
    url(r'^change_position/$',ChangePosition),
    url(r'^change_parametrs/$',ChangeParametrs),
    url(r'^check_admin_swich/$',CheckAdminSwich),
    url(r'^add_block_all_view/$', AddBlockAllView),
    url(r'^delete_ssid/$', DeleteSsid),
    url(r'^redirect_task/$',RedirectTask),
    url(r'^check_role/$',CheckRole),
)
