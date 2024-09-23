from django.urls import path
from . import views

# Create your urls here.

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.conversationInterface, name='conversation-interface'),
    path('interface-answer/', views.interfaceAnswer, name='interface-answer'),
    path('audio/<int:conversation_id>/', views.serveAudioFromDb, name='serve_audio_from_db'),
    path('latest-audio-url/', views.latestAudioUrl, name='latest_audio_url'),
    path('all-conversations/', views.allConversations, name='all-conversations'),
    path('liked-conversations/', views.likedConversations, name='liked-conversations'),
    path('get-conversation/', views.getConversation, name='get-conversation'),
    path('delete-conversation/', views.deleteConversation, name='delete-conversation'),
    path('drawing-generator/', views.drawingGenerator, name='drawing-generator'),
    path('website-review-generator/', views.websiteReviewGenerator, name='website-review-generator'),
    path('liked-reviews/', views.likedReviews, name='liked-reviews'),
    path('chat-forum/', views.chatForum, name='chat-forum'),
    path('extras-features/', views.extrasFeatures, name='extras-features'),

    path('chat-gpt/', views.chatGpt, name='chat-gpt'),
    path('chat-gpt/response/', views.response, name='response'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),

    path('update-user/', views.updateUser, name='update-user'),
    
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
]
