from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import User, Room, Topic, Message

admin.site.register(User, UserAdmin)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)