from django.conf.urls import include, url
from django.contrib import admin
from account import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.homepage),
    url(r'^account/', include('account.urls')),  
    url(r'^teacher/', include('teacher.urls')),    
    url(r'^student/', include('student.urls')),  
    url(r'^survey/', include('survey.urls')),  
    url(r'^certificate/', include('certificate.urls')),
    url(r'^show/', include('show.urls')), 
    url(r'^photologue/', include('photologue.urls')),  
    url(r'^gallery/$', TemplateView.as_view(template_name="gallery.html")),
]