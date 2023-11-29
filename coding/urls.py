from django.urls import path, include
from django.contrib import admin
from account import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('account/', include('account.urls')),  
    path('teacher/', include('teacher.urls')),    
    path('student/', include('student.urls')),  
    path('survey/', include('survey.urls')),  
    path('certificate/', include('certificate.urls')),
    path('show/', include('show.urls')), 
    path('photologue/', include('photologue.urls')),  
    path('gallery/', TemplateView.as_view(template_name="gallery.html")),
    path('annotate/', include('annotate.urls')),	
] 

