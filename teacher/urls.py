# -*- coding: UTF-8 -*-
from django.urls import re_path as url
from django.contrib.auth.decorators import login_required
from . import views
from teacher.views import ForumListView, ForumCreateView, ForumContentListView, ForumContentCreateView, ForumClassListView, ForumAllListView, ForumEditUpdateView, VideoListView

urlpatterns = [
    # 班級
    url(r'^classroom/$', login_required(views.ClassroomListView.as_view())),
    url(r'^classroom/add/$', login_required(views.ClassroomCreateView.as_view())),
    url(r'^classroom/edit/(?P<classroom_id>\d+)/$', login_required(views.classroom_edit)),
    url(r'^classroom/assistant/(?P<classroom_id>\d+)/$', login_required(views.classroom_assistant)),
    url(r'^classroom/assistant/add/(?P<classroom_id>\d+)/$', login_required(views.AssistantListView.as_view())),
    #列出所有學生帳號
    url(r'^student/list/$', views.StudentListView.as_view()),
    #加選學生
    url(r'^student/join/(?P<classroom_id>\d+)/', views.StudentJoinView.as_view()),
    url(r'^student/enroll/(?P<classroom_id>\d+)/', views.StudentEnrollView.as_view()),
    # 分組
    url(r'^group/number/(?P<pk>\d+)', views.GroupUpdate.as_view()),
    url(r'^group/size/(?P<pk>\d+)', views.GroupUpdate2.as_view()),
    url(r'^group/make/(?P<classroom_id>\d+)/(?P<action>\d+)/', views.make),
	  url(r'^group/assign/(?P<classroom_id>\d+)/', views.group_assign),
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
    url(r'^work/word/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<index>\d+)/$', views.work_word),
    url(r'^work/class/(?P<typing>\d+)/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<index>\d+)/$', views.work_class),
    url(r'^work/group/(?P<typing>\d+)/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<index>\d+)/$', views.work_group),
    url(r'^work1/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', views.work1),
    url(r'^work/ckexcel/(?P<classroom_id>\d+)/', views.work_ckexcel),
    #設定小教師
    url(r'^work/assistant/make/$', login_required(views.make_work_assistant)),
	  #評分
    url(r'^score_peer/(?P<typing>[^/]+)/(?P<lesson>[^/]+)/(?P<index>\d+)/(?P<classroom_id>\d+)/(?P<group>\d+)/$', views.score_peer),
    url(r'^scoring/(?P<typing>[^/]+)/(?P<lesson>[^/]+)/(?P<classroom_id>[^/]+)/(?P<user_id>\d+)/(?P<index>\d+)/$', views.scoring),
	  #心得
	  url(r'^memo/(?P<lesson>[^/]+)/(?P<classroom_id>[^/]+)/$', views.memo),
    url(r'^check/(?P<typing>[^/]+)/(?P<lesson>[^/]+)/(?P<unit>[^/]+)/(?P<user_id>\d+)/(?P<classroom_id>[^/]+)/$', views.check),
	  #成績
	  url(r'^grade/(?P<typing>[^/]+)/(?P<lesson>[^/]+)/(?P<unit>[^/]+)/(?P<classroom_id>\d+)/$', views.grade),
	  url(r'^grade/excel/(?P<typing>[^/]+)/(?P<lesson>[^/]+)/(?P<unit>[^/]+)/(?P<classroom_id>\d+)/$', views.grade_excel),
    # 自訂作業
    url(r'^work2/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', login_required(views.WorkListView2.as_view())),
    url(r'^work2/add/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', login_required(views.WorkCreateView2.as_view())),
    url(r'^work2/edit/(?P<lesson>\d+)(?P<classroom_id>\d+)/$', views.work_edit),
    url(r'^work2/class/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<work_id>\d+)/$', views.work_class2),
    url(r'^work2/question/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<work_id>\d+)/$', views.Science1QuestionListView.as_view()),
    url(r'^work2/question/answer/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<work_id>\d+)/(?P<q_id>\d+)$', views.Science1QuestionAnswerView.as_view()),
    url(r'^work2/question/add/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<work_id>\d+)/$', views.Science1QuestionCreateView.as_view()),
    url(r'^work2/science/(?P<classroom_id>\d+)/(?P<index>\d+)/(?P<user_id>\d+)/$', views.work2_science),
    #url(r'^work2/question/edit/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<work_id>\d+)/(?P<question_id>\d+)/$', views.work_question_edit),
    #url(r'^work2/question/delete/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<work_id>\d+)/(?P<question_id>\d+)/$', views.work_question_delete),
    # 檢核作業
    url(r'^work3/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', login_required(views.WorkListView3.as_view())),
    url(r'^work3/add/(?P<lesson>\d+)/(?P<classroom_id>\d+)/$', login_required(views.WorkCreateView3.as_view())),
    url(r'^work3/edit/(?P<lesson>\d+)(?P<classroom_id>\d+)/$', views.work_edit),
    url(r'^work3/class/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<work_id>\d+)/$', views.work_class3),
    url(r'^work3/score/(?P<lesson>\d+)/(?P<classroom_id>\d+)/(?P<work_id>\d+)/$', views.work3_score),
    # 各組小老師
    url(r'^assistant/group/(?P<typing>\d+)/(?P<classroom_id>\d+)/$', views.assistant_group),
    #設定助教
    url(r'^assistant/$', login_required(views.AssistantClassroomListView.as_view())),
    url(r'^assistant/make/$', login_required(views.assistant_make), name='make'),
    # 討論區
    url(r'^forum/(?P<categroy>\d+)/(?P<categroy_id>\d+)/$', login_required(ForumAllListView.as_view()), name='forum-all'),
    url(r'^forum/show/(?P<forum_id>\d+)/$', login_required(views.forum_show), name='forum-show'),
    url(r'^forum/edit/(?P<classroom_id>\d+)/(?P<pk>\d+)/$', login_required(ForumEditUpdateView.as_view()), name='forum-edit'),
    url(r'^forum/(?P<classroom_id>\d+)/$', login_required(ForumListView.as_view()), name='forum-list'),
    url(r'^forum/add/(?P<classroom_id>\d+)/$', login_required(ForumCreateView.as_view()), name='forum-add'),
    url(r'^forum/category/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.forum_categroy), name='forum-category'),
    url(r'^forum/deadline/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.forum_deadline), name='forum-deadline'),
    url(r'^forum/deadline/set/$', login_required(views.forum_deadline_set), name='forum-deatline-set'),
    url(r'^forum/deadline/date/$', login_required(views.forum_deadline_date), name='forum-deatline-date'),
    url(r'^forum/deadline/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.forum_deadline), name='forum-category'),
    url(r'^forum/download/(?P<content_id>\d+)/$', views.forum_download, name='forum-download'),
    url(r'^forum/content/(?P<forum_id>\d+)/$', login_required(ForumContentListView.as_view()), name='forum-content'),
    url(r'^forum/content/add/(?P<forum_id>\d+)/$', login_required(ForumContentCreateView.as_view()), name='forum-content-add'),
    url(r'^forum/content/delete/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.forum_delete), name='forum-content-delete'),
    url(r'^forum/content/edit/(?P<forum_id>\d+)/(?P<content_id>\d+)/$', login_required(views.forum_edit), name='forum-content-edit'),
    #url(r'^forum/class/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', views.forum_class, name='forum-class'),
    url(r'^forum/class/(?P<forum_id>\d+)/$',  login_required(ForumClassListView.as_view()), name='forum-class'),
    url(r'^forum/export/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/$', login_required(views.forum_export), name='forum-export'),
    url(r'^forum/grade/(?P<classroom_id>\d+)/(?P<action>\d+)/$', login_required(views.forum_grade), name='forum-grade'),
    url(r'^forum/class/switch/$', login_required(views.forum_switch), name='make'),
    url(r'^forum/publish/reject/(?P<classroom_id>\d+)/(?P<index>\d+)/(?P<user_id>\d+)', views.ForumPublishReject.as_view()),
	# 影片觀看記錄
    url(r'^event/video/(?P<classroom_id>\d+)/(?P<forum_id>\d+)/(?P<work_id>\d+)/$', views.EventVideoView.as_view()),
    url(r'^event/video/length/$', views.video_length),
		url(r'^event/video/user/(?P<classroom_id>\d+)/(?P<content_id>\d+)/(?P<user_id>\d+)/$', VideoListView.as_view()),
    #測驗卷
    url(r'^exam/(?P<classroom_id>\d+)/$', views.exam_list),
    url(r'^exam_detail/(?P<classroom_id>\d+)/(?P<student_id>\d+)/(?P<exam_id>\d+)/$', views.exam_detail),
]