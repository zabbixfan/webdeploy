"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
#from app1 import views as app1_views1
from shell import views as shell_views
from auto_install import views as auto
urlpatterns = [
    url(r'^admin/', admin.site.urls),
#    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': '/opt/web/app1/templates/css/' }),
#    url(r'^js/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': '/opt/web/app1/templates/js/' }),
#    url(r'^img/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': '/opt/web/app1/img/' }),
    url(r'^login', auto.my_login), 
    url(r'^logout', auto.my_logout), 
    url(r'^zcgl', auto.zcgl), 
    url(r'^shell', shell_views.shell), 
    #url(r'^$',app1_views.index),
    url(r'^deploy',auto.deploy),
    url(r'^module_list/$',auto.module_list),
    url(r'^app_list',auto.app_list),
    url(r'^server_list',auto.server_list),
    url(r'^commit',auto.commit),
    url(r'^rollback',auto.rollback),
    url(r'^$',auto.index),
    url(r'^log$',auto.log),
    url(r'^logdetail',auto.ldetail)
]
