from django.contrib import admin
from account.models import County, Zone, School, Profile, Message, Visitor,MessagePoll

admin.site.register(County)
admin.site.register(Zone)
admin.site.register(School)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Visitor)
admin.site.register(MessagePoll)
