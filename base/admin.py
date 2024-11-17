from django.contrib import admin
from .models import Conversation, DrawingDatabase, Room, Topic, Message, WebsiteReview, BlogPost #UserManager, User

# Register your models here.

#admin.site.register(UserManager)
#admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(DrawingDatabase)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(WebsiteReview)
admin.site.register(BlogPost)
