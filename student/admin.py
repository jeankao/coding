from django.contrib import admin
from student.models import Work, Enroll, WorkFile

admin.site.register(Work)
admin.site.register(WorkFile)
admin.site.register(Enroll)
