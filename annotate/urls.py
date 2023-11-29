# -*- coding: UTF-8 -*-
from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.root)),
    path('annotations', login_required(views.annotations)),
    # path('annotations/(?P<annotation_id>\d+)/?$', login_required(views.single_annotation)),
    path('annotations/<int:annotation_id>/', login_required(views.single_annotation)),
    path('search', login_required(views.search)),
]