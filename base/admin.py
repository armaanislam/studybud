from django.contrib import admin
from .models import Room, Topic, Message #User is set by default

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
