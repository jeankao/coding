# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
  url(r'^$', login_required(views.root)),
  url(r'^annotations$', login_required(views.annotations)),
  url(r'^annotations/(?P<annotation_id>\d+)/?$', login_required(views.single_annotation)),
  url(r'^search$', login_required(views.search)),
]