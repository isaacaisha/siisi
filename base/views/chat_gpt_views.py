import os
import io
import datetime
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# 2 Factor Authentication integration
from django_otp.decorators import otp_required

# Models from the same Django app
from ..models import Conversation
from ..forms import TextAreaForm, TextAreaDrawingIndex

# Import helper functions from utils_chat_gpt
from .utils_chat_gpt import (
    find_most_relevant_conversation,
    generate_conversation_context,
    handle_llm_response,
    save_to_database
)

# Langchain and OpenAI integration
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Conversation memory
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory

# Language detection
from langdetect import detect

# Date and time handling
from datetime import datetime


openai = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(temperature=0.0, model="gpt-4o")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)
memory_summary = ConversationSummaryBufferMemory(llm=llm, max_token_limit=3)


# View for the VIP page, requiring 2FA status
@login_required
@otp_required
def conversationInterface(request):
    writing_text_form = TextAreaForm()
    drawing_form = TextAreaDrawingIndex()
    user_input = None
    answer = None
    latest_conversation = []

    if request.method == "POST":
        user_input = request.POST.get('writing_text', '')
        answer = conversation.predict(input=user_input)
        latest_conversation = Conversation.objects.filter(owner_id=request.user.id).order_by('-id')

    context = {
        'writing_text_form': writing_text_form,
        'drawing_form': drawing_form,
        'user_input': user_input,
        'answer': answer,
        'memory_buffer': memory.buffer_as_str,
        'memory_load': memory.load_memory_variables({}),
        'latest_conversation': latest_conversation,
        'date': datetime.now().strftime("%a %d %B %Y"),
    }
    return render(request, 'base/conversation_interface.html', context)


def interfaceAnswer(request):
    if request.method == 'POST':
        # Get the user's input from the POST request
        user_input = request.POST.get('prompt', '')
        
        # Detect the language of the input
        detected_lang = detect(user_input)
        user_email = request.user.email

        # Check if the user is 'medusadbt@gmail.com'
        if user_email == 'medusadbt@gmail.com':
            print("Using embedding method for medusadbt@gmail.com")
            # Fetch 91 most recent conversations
            user_conversations = Conversation.objects.filter(owner=request.user).order_by('-created_at')[:91]

            # Generate embeddings from stored data
            embeddings = [
                np.frombuffer(memory.embedding, dtype=float) for memory in user_conversations if memory.embedding is not None
            ]

            # If no embeddings exist, handle new user
            if not embeddings:
                assistant_reply, audio_data, response, flash_message = handle_llm_response(user_input, None, detected_lang)
                save_to_database(request.user, user_input, response, audio_data)

                return JsonResponse({
                    "answer_text": assistant_reply,
                    "detected_lang": detected_lang,
                    "flash_message": flash_message
                })

            # Find the most relevant conversation
            index, similarity = find_most_relevant_conversation(user_input, embeddings)
            
            # Convert index to standard Python int
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
            # Default case for all other users
            print(f"User {user_email} is not using the embedding method")
            user_conversations = Conversation.objects.filter(owner=request.user).order_by('-created_at')[:3]
            conversation_context = generate_conversation_context(user_input, user_conversations)

        # Get the response from the language model
        assistant_reply, audio_data, response, flash_message = handle_llm_response(user_input, conversation_context, detected_lang)
        save_to_database(request.user, user_input, response, audio_data)

        # Return the response as JSON
        return JsonResponse({
            "answer_text": assistant_reply,
            "detected_lang": detected_lang,
            "flash_message": flash_message
        })
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def serveAudioFromDb(request, conversation_id):
    """Serve audio file from a specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if conversation.audio_datas:
        audio_data = io.BytesIO(conversation.audio_datas)
        return FileResponse(
            audio_data,
            content_type='audio/mpeg',
            filename=f"audio_{conversation_id}.mp3"
        )
    else:
        return HttpResponse("Audio not found", status=404)


def latestAudioUrl(request):
    """Provide the URL for the latest audio in user's conversation"""
    latest_conversation = Conversation.objects.filter(owner=request.user).order_by('-created_at').first()

    if latest_conversation and latest_conversation.audio_datas:
        audio_url = reverse('serve_audio_from_db', args=[latest_conversation.id])
        return JsonResponse({"audio_url": audio_url})
    else:
        return JsonResponse({"error": "No audio found"}, status=404)
    