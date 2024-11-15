from .auth_views import loginPage, logoutUser, logoutUserToChat, registerPage, password_reset_request, password_reset_done, password_reset_confirm, password_reset_complete

from .chat_gpt_views import conversationInterface, interfaceAnswer, serveAudioFromDb, latestAudioUrl
from .utils_chat_gpt import generate_conversation_context, handle_llm_response, adjust_conversation_context, get_llm_response, extract_assistant_reply, clean_assistant_reply, handle_language_support, generate_audio_data, find_most_relevant_conversation, save_to_database
from .utils_gpt_convers import allConversations, updateLike, likedConversations, ConversationById, ConversationSelected, deleteConversation, conversationsDatabase, deleteData
from .chat_forum_views import chatForum, room
from .profile_views import updateUser, userProfile
from .utils_chat_forum import createRoom, updateRoom, deleteRoom, deleteMessage, topicsPage, activityPage

from .extras_feats import drawingGenerator, websiteReviewGenerator, likedReviews, extrasFeatures

from ..templatetags.custom_filters import pretty_json
