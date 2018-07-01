from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # post views
    url(r'^list/(?P<classroom_id>[^/]+)/$', login_required(views.ShowListView.as_view())),
	  url(r'^group/delete/(?P<group_id>[^/]+)/(?P<round_id>[^/]+)/$', views.group_delete), 	
    url(r'^group/enroll/(?P<round_id>[^/]+)/(?P<group_id>[^/]+)/$', views.group_enroll),   
    url(r'^group/size/(?P<round_id>[^/]+)/$', views.group_size),     
    url(r'^group/open/(?P<round_id>[^/]+)/(?P<action>[^/]+)/$', views.group_open), 	
    url(r'^group/add/(?P<round_id>[^/]+)/$', views.group_add),     
    url(r'^group/(?P<round_id>[^/]+)/$', views.group),     
    url(r'^group/submit/(?P<round_id>[^/]+)/(?P<group_show>[^/]+)/$', login_required(views.ShowUpdateView.as_view())),    
    url(r'^detail/(?P<round_id>[^/]+)/(?P<show_id>[^/]+)/$', login_required(views.ReviewUpdateView.as_view())),      
    url(r'^score/(?P<show_id>[^/]+)/$', login_required(views.ReviewListView.as_view())),  	
    url(r'^rank/(?P<rank_id>[^/]+)/(?P<round_id>[^/]+)/$', login_required(views.RankListView.as_view())), 
    url(r'^teacher/(?P<classroom_id>[^/]+)/$', views.classroom),
    url(r'^teacher/comment/(?P<round_id>[^/]+)/$', views.commentall),	
    url(r'^teacher/comment/(?P<round_id>[^/]+)/(?P<user_id>[^/]+)/$', views.comment),		
    url(r'^teacher/grading/(?P<round_id>[^/]+)/$', login_required(views.TeacherListView.as_view())),	
    url(r'^teacher/scoring/(?P<round_id>[^/]+)/$', login_required(views.ScoreListView.as_view())),		
    url(r'^teacher/add/(?P<classroom_id>[^/]+)/$', views.round_add),		
    url(r'^gallery/(?P<category>[^/]+)/$', views.GalleryListView.as_view()),    
    url(r'^gallery/make/$', views.make, name='make'),   	
    url(r'^gallery/detail/(?P<show_id>[^/]+)/$', views.GalleryDetail),  
    url(r'^download/(?P<show_id>\d+)/(?P<showfile_id>\d+)/$', views.show_download),	
    url(r'^excel/(?P<round_id>[^/]+)/$', views.excel),
    url(r'^zip/(?P<round_id>[^/]+)/$', views.zip),	
]