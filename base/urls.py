from django.urls import path
from .views import (
    loginPage, logoutUser, logoutUserToChat, registerPage,
    password_reset_request, password_reset_done, password_reset_confirm, password_reset_complete,
    conversationInterface, interfaceAnswer, serveAudioFromDb, latestAudioUrl,
    allConversations, updateLike, likedConversations,
    ConversationById, ConversationSelected,deleteConversation,
    conversationsDatabase, deleteData, chatForum, 
    drawingGenerator, websiteReviewGenerator, likedReviews, extrasFeatures, 
    updateUser, userProfile, room,
    createRoom, updateRoom, deleteRoom, deleteMessage,
    topicsPage, activityPage
)

# Create your urls here.

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('logout-to-chat/', logoutUserToChat, name='logout-to-chat'),
    path('register/', registerPage, name='register'),
    
    # Password Reset URLs
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete, name='password_reset_complete'),

    path('conversation-interface', conversationInterface, name='conversation-interface'),
    path('interface-answer/', interfaceAnswer, name='interface-answer'),
    path('audio/<int:conversation_id>/', serveAudioFromDb, name='serve_audio_from_db'),
    path('latest-audio-url/', latestAudioUrl, name='latest_audio_url'),
    path('all-conversations/', allConversations, name='all-conversations'),
    path('update-like/<int:conversation_id>/', updateLike, name='update-like'),
    path('liked-conversations/', likedConversations, name='liked-conversations'),
    path('conversation-selected/<int:conversation_id>/', ConversationSelected, name='conversation_selected'),
    path('conversation-by-id/', ConversationById, name='conversation-by-id'),
    path('delete-conversation/', deleteConversation, name='delete-conversation'),
    path('databse-conversation/', conversationsDatabase, name='databse-conversation'),
    path('delete-data/', deleteData, name='delete-data'),

    path('', chatForum, name='chat-forum'),
    path('drawing-generator/', drawingGenerator, name='drawing-generator'),
    path('website-review-generator/', websiteReviewGenerator, name='website-review-generator'),
    path('liked-reviews/', likedReviews, name='liked-reviews'),
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
