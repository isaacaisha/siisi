# base/views/chat_gpt_views.py

import io
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Date and time handling
from django.utils import timezone

# 2 Factor Authentication integration
from django_otp.decorators import otp_required

# Models and Forms
from ..models import Conversation
from ..forms import TextAreaForm

# Import helper functions from utils_chat_gpt
from .utils_chat_gpt import (
    find_most_relevant_conversation,
    generate_conversation_context,
    handle_llm_response,
    save_to_database, detect
)


# Function to render the conversation interface
@login_required(login_url='login')
def conversationInterface(request):
    """Render the main interface for conversation."""
    writing_text_form = TextAreaForm()
    user_input = None
    answer = None
    latest_conversation = []

    if request.method == "POST":
        user_input = request.POST.get('writing_text', '')
        answer = handle_llm_response(user_input, None, None)[0]
        latest_conversation = Conversation.objects.filter(owner=request.user).order_by('-created_at')

    context = {
        'writing_text_form': writing_text_form,
        'user_input': user_input,
        'answer': answer,
        'latest_conversation': latest_conversation,
        'date': timezone.now().strftime("%a %d %B %Y"),
    }
    return render(request, 'base/conversation_interface.html', context)


# Function to handle interface answers
def interfaceAnswer(request):
    """Process and respond to user input from the conversation interface."""
    if request.method == 'POST':
        user_input = request.POST.get('prompt', '')
        detected_lang = detect(user_input)
        user_email = request.user.email

        if user_email == 'medusadbt@gmail.com':
            print("Using embedding method for medusadbt@gmail.com")
            # Fetch recent conversations and generate embeddings
            user_conversations = Conversation.objects.filter(owner=request.user).order_by('-created_at')[:91]
            embeddings = [
                np.frombuffer(memory.embedding, dtype=float) for memory in user_conversations if memory.embedding is not None
            ]

            if not embeddings:
                # Handle case where no embeddings exist
                assistant_reply, audio_data, response, flash_message = handle_llm_response(user_input, None, detected_lang)
                save_to_database(request.user, user_input, response, audio_data)
                return JsonResponse({
                    "answer_text": assistant_reply,
                    "detected_lang": detected_lang,
                    "flash_message": flash_message
                })

            # Find most relevant conversation
            index, similarity = find_most_relevant_conversation(user_input, embeddings)
            most_relevant_memory = user_conversations[int(index)]

            conversation_context = {
                "user_name": request.user.username,
                "user_message": user_input,
                "most_relevant_conversation": {
                    "user_message": most_relevant_memory.user_message,
                    "llm_response": most_relevant_memory.llm_response,
                    "created_at": str(most_relevant_memory.created_at),
                    "similarity": similarity
                },
                "previous_conversations": [
                    {
                        "user_message": memory.user_message,
                        "llm_response": memory.llm_response,
                        "created_at": str(memory.created_at)
                    } for memory in user_conversations
                ]
            }
        else:
            # Default case for other users
            print(f"User {user_email} is not using the embedding method")
            user_conversations = Conversation.objects.filter(owner=request.user).order_by('-created_at')[:3]
            
            # Generate conversation context
            conversation_context = generate_conversation_context(user_input, user_conversations)
            print(f"conversation_context:\n{conversation_context}")

        # Now pass conversation_context to the LLM response handler
        assistant_reply, audio_data, response, flash_message = handle_llm_response(user_input, conversation_context, detected_lang)
        save_to_database(request.user, user_input, response, audio_data)

        return JsonResponse({
            "answer_text": assistant_reply,
            "detected_lang": detected_lang,
            "flash_message": flash_message
        })
    return JsonResponse({"error": "Invalid request method"}, status=400)


# Function to serve audio from the database
def serveAudioFromDb(request, conversation_id):
    """Serve audio file from a specific conversation."""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if conversation.audio_datas:
        audio_data = io.BytesIO(conversation.audio_datas)
        return FileResponse(
            audio_data,
            content_type='audio/mpeg',
            filename=f"audio_{conversation_id}.mp3"
        )
    return HttpResponse("Audio not found", status=404)


# Function to provide the URL for the latest audio
def latestAudioUrl(request):
    """Provide the URL for the latest audio in user's conversations."""
    latest_conversation = Conversation.objects.filter(owner=request.user).order_by('-created_at').first()
    if latest_conversation and latest_conversation.audio_datas:
        audio_url = reverse('serve_audio_from_db', args=[latest_conversation.id])
        return JsonResponse({"audio_url": audio_url})
    return JsonResponse({"error": "No audio found"}, status=404)


# Super User page requiring 2FA
@otp_required
@login_required(login_url='two_factor:login')
def superuserViews(request):
    """Render the superuser views page, restricted by 2FA."""
    context = {'date': timezone.now().strftime("%a %d %B %Y")}
    return render(request, 'base/superuser-views.html', context)
