# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^select/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', views.select),
    url(r'^pre_survey1/$', views.pre_survey1),
    url(r'^post_survey1/$', views.post_survey1),  
    url(r'^pre_result1/(?P<classroom_id>\d+)/$', views.pre_result1),
    url(r'^post_result1/(?P<classroom_id>\d+)/$', views.post_result1),  
    url(r'^pre_survey1/teacher/(?P<classroom_id>\d+)/$', views.pre_teacher1),  
    url(r'^post_survey1/teacher/(?P<classroom_id>\d+)/$', views.post_teacher1),    
    url(r'^pre_survey2/$', views.pre_survey2),
    url(r'^post_survey2/$', views.post_survey2), 
    url(r'^pre_result2/(?P<classroom_id>\d+)/$', views.pre_result2),
    url(r'^post_result2/(?P<classroom_id>\d+)/$', views.post_result2),   
    url(r'^pre_survey2/teacher/(?P<classroom_id>\d+)/$', views.pre_teacher2),  
    url(r'^post_survey2/teacher/(?P<classroom_id>\d+)/$', views.post_teacher2),   
    url(r'^pre_survey5/$', views.pre_survey5),
    url(r'^post_survey5/$', views.post_survey5), 
    url(r'^pre_result5/(?P<classroom_id>\d+)/$', views.pre_result5),
    url(r'^post_result5/(?P<classroom_id>\d+)/$', views.post_result5),   
    url(r'^pre_survey5/teacher/(?P<classroom_id>\d+)/$', views.pre_teacher5),  
    url(r'^post_survey5/teacher/(?P<classroom_id>\d+)/$', views.post_teacher5),    
]