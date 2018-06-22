from django.conf.urls import include, url
from django.contrib import admin
from account import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.homepage),
    url(r'^account/', include('account.urls')),  
    url(r'^teacher/', include('teacher.urls')),    
    url(r'^student/', include('student.urls')),  
    url(r'^certificate/', include('certificate.urls')),
]