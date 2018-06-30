# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^lessons/(?P<subject_id>[^/]+)/$', views.lessons),
    url(r'^lesson/(?P<lesson>[^/]+)/$', views.lesson),
    # 選課
    url(r'^classroom/enroll/(?P<classroom_id>[^/]+)/$', views.classroom_enroll),      
    url(r'^classroom/add/$', views.classroom_add),  
    url(r'^classroom/$', views.classroom),
     url(r'^classroom/seat/(?P<enroll_id>\d+)/(?P<classroom_id>\d+)/$', views.seat_edit),
    # 同學
    url(r'^classmate/(?P<classroom_id>\d+)/$', views.classmate), 
    url(r'^loginlog/(?P<user_id>\d+)/$', views.LoginLogListView.as_view()),     
    # 分組
    url(r'^group/enroll/(?P<classroom_id>[^/]+)/(?P<group_id>[^/]+)/$', views.group_enroll),    
    url(r'^group/add/(?P<classroom_id>[^/]+)/$', views.group_add),     
    url(r'^group/(?P<classroom_id>[^/]+)/$', views.group),   
    url(r'^group/size/(?P<classroom_id>[^/]+)/$', views.group_size),      
    url(r'^group/open/(?P<classroom_id>[^/]+)/(?P<action>[^/]+)/$', views.group_open),     
    url(r'^group/delete/(?P<group_id>[^/]+)/(?P<classroom_id>[^/]+)/$', views.group_delete),
    #公告
    url(r'^announce/(?P<classroom_id>\d+)/$', login_required(views.AnnounceListView.as_view())),
    #作業
    url(r'^work/(?P<typing>\d+)/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', login_required(views.work_list)),  
    url(r'^work/submit/(?P<typing>\d+)/(?P<lesson>\d+)/(?P<index>\d+)/$', views.submit),
    url(r'^work/show/(?P<typing>\d+)/(?P<lesson>\d+)/(?P<index>\d+)/(?P<user_id>\d+)/$', views.show),      
    url(r'^work/memo/(?P<typing>\d+)/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<index>\d+)/$', views.memo), 
     url(r'^work/rank/(?P<typing>\d+)/(?P<lesson>\d+)/(?P<index>\d+)/$', views.rank), 
    url(r'^work/download/(?P<index>\d+)/(?P<user_id>\d+)/(?P<workfile_id>\d+)/$', views.work_download), 
     url(r'^work/list/(?P<lesson>\d+)/$', views.WorkListView.as_view()),     
     url(r'^work/day/(?P<lesson>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<date>\d+)/$', views.WorkDayListView.as_view()),       
    #查詢該作業分組小老師
    url(r'^group/work/(?P<lesson>\d+)/(?P<index>\d+)/(?P<classroom_id>\d+)$', views.work_group),  		
    url(r'^work/answer/(?P<lesson>\d+)/(?P<index>\d+)/$', views.answer),
    url(r'^work/answer_watch/(?P<lesson>\d+)/(?P<index>\d+)/$', views.answer_watch),	
    #url(r'^work1/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', views.work1),  	
    # 作業進度查詢
    url(r'^progress/(?P<typing>\d+)/(?P<lesson>\d+)/(?P<unit>\d+)/(?P<classroom_id>\d+)/$', views.progress),  
    #測驗
    url(r'^exam/$', views.exam),      
    url(r'^exam_check/$', views.exam_check),     
    url(r'^exam/score/$', views.exam_score),   
]