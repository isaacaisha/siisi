from django.urls import path
from .views import (
    superuserViews,
    conversationInterface, interfaceAnswer, serveAudioFromDb, latestAudioUrl,
    allConversations, updateLike, likedConversations,
    ConversationById, ConversationSelected, deleteConversation,
    drawingGenerator, websiteReviewGenerator, likedReviews, extrasFeatures, 
)

# Create your urls here.

urlpatterns = [
    path('superuser-views', superuserViews, name='superuser-views'),

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

    path('delete-conversation/', deleteConversation, name='delete-conversation'),
    
    path('extras-features/', extrasFeatures, name='extras-features'),

    path('drawing-generator/', drawingGenerator, name='drawing-generator'),

    path('website-review-generator/', websiteReviewGenerator, name='website-review-generator'),
    path('liked-reviews/', likedReviews, name='liked-reviews'),
]
