# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^hoc/$', views.upload_pic),   
    url(r'^show/(?P<lesson>\d+)/(?P<unit>\d+)/(?P<enroll_id>\d+)/$', views.show),   
    url(r'^make/$', views.make, name='make'),
    url(r'^(?P<lesson>[^/]+)/(?P<unit>[^/]+)/(?P<enroll_id>[^/]+)/(?P<action>[^/]+)/$', views.certificate), 
    url(r'^cert/classroom/(?P<lesson>\d+)/(?P<unit>\d+)/(?P<classroom_id>\d+)/$', views.classroom),
]