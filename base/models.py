from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(max_length=199, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    # Use email as the unique identifier for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Link the custom manager to the User model
    objects = UserManager()

    def __str__(self):
        return self.email


class Topic(models.Model):
    name = models.CharField(max_length=199)

    def __str__(self):
        return self.name
    

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
        return f"{self.user_name} - {self.created_at}"
    

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=199)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:59]


class DrawingDatabase(models.Model):
    user_name = models.CharField(max_length=73)
    user_prompt = models.TextField()
    image_url = models.TextField()
    analysis_text = models.TextField(null=True, blank=True)
    audio_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.created_at}"


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
        return f"{self.site_url} - {self.created_at}"


class BlogPost(models.Model):
    youtube_title = models.CharField(max_length=255)
    youtube_link = models.URLField(max_length=255)
    generated_content = models.TextField()
    audio_data = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    def __str__(self):
        return f"{self.youtube_title} - {self.created_at}"
