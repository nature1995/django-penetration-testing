from django.conf.urls import url
from django.urls  import path

from asset import views
urlpatterns = [
    url(r'^domain_list/$', views.domain_list, name='domain_list'),
    url(r'^domain_list/add/$', views.domain_manage, name='domain_add'),
    url(r'^domain_list/edit/(?P<aid>\d+)/(?P<action>[\w-]+)/$', views.domain_manage, name='domain_manage'),
]