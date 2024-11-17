from django.contrib import admin
from .models import Conversation, DrawingDatabase, WebsiteReview, BlogPost

# Register your models here.

admin.site.register(Conversation)
admin.site.register(DrawingDatabase)
admin.site.register(WebsiteReview)
admin.site.register(BlogPost)
