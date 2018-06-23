# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^pre_survey1/$', views.pre_survey1),
    url(r'^post_survey1/$', views.post_survey1),  
    url(r'^pre_result1/(?P<classroom_id>\d+)/$', views.pre_result1),
    url(r'^post_result1/(?P<classroom_id>\d+)/$', views.post_result1),  
    url(r'^pre_survey1/teacher/(?P<classroom_id>\d+)/$', views.pre_teacher1),  
    url(r'^post_survey1/teacher/(?P<classroom_id>\d+)/$', views.post_teacher1),    
]