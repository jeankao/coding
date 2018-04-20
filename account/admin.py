from django.contrib import admin
from account.models import County, Zone, School, Profile, Message

admin.site.register(County)
admin.site.register(Zone)
admin.site.register(School)
admin.site.register(Profile)
admin.site.register(Message)