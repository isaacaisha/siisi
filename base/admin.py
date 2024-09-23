from django.contrib import admin
from .models import ChatData, Room, Topic, Message, User # Conversation

# Register your models here.

# admin.site.register(Conversation)

@admin.register(ChatData)
class ChatDataAdmin(admin.ModelAdmin):
    list_display = ('message', 'response', 'created_at')

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
