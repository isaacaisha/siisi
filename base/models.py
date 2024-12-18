# base/models.py

from django.db import models
from django.utils.translation import gettext as _

from two_factor_auth.models import User

# Create your models here.


class Conversation(models.Model):
    user_name = models.CharField(max_length=55)
    user_message = models.TextField()
    llm_response = models.TextField()
    audio_datas = models.BinaryField(blank=True, null=True)
    embedding = models.BinaryField(blank=True, null=True)
    conversations_summary = models.TextField()
    liked = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')

    def __str__(self):
        return _("{} - {}").format(self.user_name, self.created_at)


class DrawingDatabase(models.Model):
    user_name = models.CharField(max_length=73)
    user_prompt = models.TextField()
    image_url = models.TextField()
    analysis_text = models.TextField(null=True, blank=True)
    audio_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _("{} - {}").format(self.user_name, self.created_at)


class WebsiteReview(models.Model):
    site_url = models.URLField(max_length=9991)
    site_image_url = models.TextField()
    tts_url = models.TextField(null=True, blank=True)
    feedback = models.TextField(default='', blank=True)
    liked = models.IntegerField(default=0)
    user_rating = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='website_reviews')

    def __str__(self):
        return _("{} - {}").format(self.site_url, self.created_at)
    

class BlogPost(models.Model):
    youtube_title = models.CharField(max_length=255)
    youtube_link = models.URLField(max_length=255)
    generated_content = models.TextField()
    audio_data = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    def __str__(self):
        return _("{} - {}").format(self.youtube_title, self.created_at)
