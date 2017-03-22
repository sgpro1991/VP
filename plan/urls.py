"""plan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#import django
from django.conf.urls import url, include
from django.contrib import admin

from django.views.i18n import JavaScriptCatalog

from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from plan import settings
"""
js_info_dict = {
#    'domain': 'djangojs',
    'domain': 'django',
    'packages': ('recurrence', ),
}
"""
import debug_toolbar

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^block/', include('blocks.urls')),
    url(r'^number/', include('number.urls')),
    url(r'^doc/', include('workflow.urls')),
    url(r'^api/',include('api.urls')),
    url(r'^users/',include('users.urls')),
    url(r'^scheduler/',include('scheduler.urls')),
    url(r'^claim/',include('claim.urls')),
    #url(r'^jsi18n/$', django.views.i18n.javascript_catalog, js_info_dict),
    #url(r'^jsi18n/$', django.views.i18n.javascript_catalog, js_info_dict),
    #url(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict, name='javascript-catalog'),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^$', RedirectView.as_view(url='/number/')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^__debug__/', include(debug_toolbar.urls)),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






########################
