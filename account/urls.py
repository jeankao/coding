# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # post views
    url(r'^dashboard/(?P<action>\d+)/$',  views.MessageListView.as_view()),  
    #登入
    url(r'^login/(?P<role>\d+)/$', views.user_login),  
    #註冊帳號
    url(r'^register/$', views.register),
    #註冊學校
    url(r'^register_school/$', views.register_school),  
    #登出
    url(r'^logout/$',auth_views.logout),
    #列出所有帳號
    url(r'^userlist/(?P<group>\d+)/$', views.UserListView.as_view()),
    # 作者
    url(r'^author/$', views.author),
    # 關於我們
    url(r'^about/$', views.about),  
    # 連絡我們
    url(r'^contact/$', views.contact),
    # 教材研發
    url(r'^people/$', views.people),	
    # 數據統計 
    url(r'^statics/lesson/$', views.LessonCountView.as_view()),      
    #訪客
    url(r'^statics/login/$', views.VisitorListView.as_view()),    
    url(r'^statics/login/log/(?P<visitor_id>\d+)/$', login_required(views.VisitorLogListView.as_view())),   
    # 讀取訊息
    url(r'^message/(?P<messagepoll_id>\d+)/$', views.message),  
    #個人檔案
    url(r'^profile/(?P<user_id>\d+)/$', views.profile),    
    #修改密碼
    url(r'^password-change/$', auth_views.password_change, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),    
    url(r'^password/(?P<user_id>\d+)/$', views.password),
    #修改真實姓名
    url(r'^realname/(?P<user_id>\d+)/$', views.adminrealname),    
    url(r'^realname/$', views.realname, name='realname'), 
    #修改學校
    url(r'^school/$', views.adminschool),     
    #修改信箱
    url(r'^email/$', views.adminemail),    
    #積分記錄
    url(r'^log/(?P<kind>\d+)/(?P<user_id>\d+)/$', views.LogListView.as_view()),	     
    #管理介面 
    url(r'^admin/$', login_required(views.admin)),     
    url(r'^admin/schools/$', views.schools),       
    url(r'^admin/school/(?P<pk>\d+)/$', login_required(views.SchoolUpdateView.as_view())),    
    #設定教師
    url(r'^teacher/make/$', login_required(views.make)), 
    url(r'^teacher/apply/$', login_required(views.teacher_apply)),   
    # 列所出有圖像
    url(r'^avatar/$', views.avatar),  
    # 私訊
    url(r'^line/$', login_required(views.LineListView.as_view())),    
    url(r'^line/class/(?P<classroom_id>\d+)/$', login_required(views.LineClassListView.as_view())),        
    url(r'^line/add/(?P<classroom_id>\d+)/(?P<user_id>\d+)/$', login_required(views.LineCreateView.as_view())),
    url(r'^line/reply/(?P<classroom_id>\d+)/(?P<user_id>\d+)/(?P<message_id>\d+)/$', login_required(views.LineReplyView.as_view())),	
    url(r'^line/detail/(?P<classroom_id>\d+)/(?P<message_id>\d+)/$', login_required(views.line_detail)),
	  url(r'^line/download/(?P<file_id>\d+)/$', views.line_download, name='forum-download'), 
	  url(r'^line/showpic/(?P<file_id>\d+)/$', login_required(views.line_showpic), name='forum-showpic'), 
    #url(r'^teacher/$', login_required(views.TeacherPostCreateView.as_view())),	  
]