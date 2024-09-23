from django.urls import path
from .views import (
    loginPage, logoutUser, registerPage,
    conversationInterface, interfaceAnswer, serveAudioFromDb, latestAudioUrl,
    allConversations, likedConversations, getConversation, deleteConversation,
    drawingGenerator, websiteReviewGenerator, likedReviews, extrasFeatures,
    chatForum, updateUser, userProfile, room,
    createRoom, updateRoom, deleteRoom, deleteMessage,
    topicsPage, activityPage
)

# Create your urls here.

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),

    path('', conversationInterface, name='conversation-interface'),
    path('interface-answer/', interfaceAnswer, name='interface-answer'),
    path('audio/<int:conversation_id>/', serveAudioFromDb, name='serve_audio_from_db'),
    path('latest-audio-url/', latestAudioUrl, name='latest_audio_url'),
    path('all-conversations/', allConversations, name='all-conversations'),
    path('liked-conversations/', likedConversations, name='liked-conversations'),
    path('get-conversation/', getConversation, name='get-conversation'),
    path('delete-conversation/', deleteConversation, name='delete-conversation'),
    path('drawing-generator/', drawingGenerator, name='drawing-generator'),
    path('website-review-generator/', websiteReviewGenerator, name='website-review-generator'),
    path('liked-reviews/', likedReviews, name='liked-reviews'),
    path('chat-forum/', chatForum, name='chat-forum'),
    path('extras-features/', extrasFeatures, name='extras-features'),

    path('room/<str:pk>/', room, name='room'),
    path('profile/<str:pk>/', userProfile, name='user-profile'),
    
    path('create-room/', createRoom, name='create-room'),
    path('update-room/<str:pk>/', updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', deleteMessage, name='delete-message'),

    path('update-user/', updateUser, name='update-user'),
    
    path('topics/', topicsPage, name='topics'),
    path('activity/', activityPage, name='activity'),
]
