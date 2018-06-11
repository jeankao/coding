# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [  
    # 班級
    url(r'^classroom/$', login_required(views.ClassroomListView.as_view())),
    url(r'^classroom/add/$', login_required(views.ClassroomCreateView.as_view())),
    url(r'^classroom/edit/(?P<classroom_id>\d+)/$', login_required(views.classroom_edit)),
    url(r'^classroom/assistant/(?P<classroom_id>\d+)/$', login_required(views.classroom_assistant)),  
    url(r'^classroom/assistant/add/(?P<classroom_id>\d+)/$', login_required(views.AssistantListView.as_view())),       
    #列出所有學生帳號
    url(r'^student/list/$', views.StudentListView.as_view()),    	
	  #大量匯入帳號
    url(r'^import/upload$', login_required(views.import_sheet), name='import_upload'),   	
    url(r'^import/student$', login_required(views.import_student), name='import_user'),  	
    #修改資料
    url(r'^password/(?P<user_id>\d+)/$', views.password),
    url(r'^realname/(?P<user_id>\d+)/$', views.realname),    	
    #設定助教
    #url(r'^assistant/$', login_required(views.AssistantClassroomListView.as_view())),  
    #url(r'^assistant/make/$', login_required(views.assistant_make), name='make'),     
    # 退選
    url(r'^unenroll/(?P<enroll_id>\d+)/(?P<classroom_id>\d+)/$', login_required(views.unenroll)),  	
    #公告
    url(r'^announce/(?P<classroom_id>\d+)/$', login_required(views.AnnounceListView.as_view())),
    url(r'^announce/add/(?P<classroom_id>\d+)/$', login_required(views.AnnounceCreateView.as_view())),  
    url(r'^announce/detail/(?P<message_id>\d+)/$', views.announce_detail), 
    # 作業
    url(r'^work/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', login_required(views.WorkListView.as_view())),  
    url(r'^work/class/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<index>\d+)/$', views.work_class),
    url(r'^work1/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', views.work1),    
    #設定小教師
    url(r'^work/assistant/make/$', login_required(views.make)), 
	  #評分
    url(r'^score_peer/(?P<lesson>[^/]+)/(?P<index>\d+)/(?P<classroom_id>\d+)/(?P<group>\d+)/$', views.score_peer),     
    url(r'^scoring/(?P<lesson>[^/]+)/(?P<classroom_id>[^/]+)/(?P<user_id>\d+)/(?P<index>\d+)/$', views.scoring), 
	  #心得
	  url(r'^memo/(?P<lesson>[^/]+)/(?P<classroom_id>[^/]+)/$', views.memo), 
    url(r'^check/(?P<lesson>[^/]+)/(?P<unit>[^/]+)/(?P<user_id>\d+)/(?P<classroom_id>[^/]+)/$', views.check), 
	  #成績
	  url(r'^grade/(?P<lesson>[^/]+)/(?P<classroom_id>\d+)/$', views.grade),	
		 
]