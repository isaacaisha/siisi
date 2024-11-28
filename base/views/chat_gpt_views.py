import os
import io
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# 2 Factor Authentication integration
from django_otp.decorators import otp_required

# Models and Forms
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
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Conversation memory
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory

# Language detection
from langdetect import detect

# Date and time handling
from django.utils import timezone

# OpenAI API and LangChain setup
openai = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(temperature=0.0, model="gpt-4o")
memory = ConversationBufferMemory(k=3)

# Define a simple prompt template
prompt = PromptTemplate(input_variables=["input"], template="{input}")
conversation = LLMChain(llm=llm, memory=memory, prompt=prompt, verbose=False)
memory_summary = ConversationSummaryBufferMemory(llm=llm, max_token_limit=3)

# Function to render the conversation interface
@login_required(login_url='login')
def conversationInterface(request):
    """Render the main interface for conversation."""
    writing_text_form = TextAreaForm()
    user_input = None
    answer = None
    latest_conversation = []

    if request.method == "POST":
        # Process user input and generate a response
        user_input = request.POST.get('writing_text', '')
        answer = conversation.predict(input=user_input)
        # Fetch the user's latest conversations
        latest_conversation = Conversation.objects.filter(owner_id=request.user.id).order_by('-id')

    context = {
        'writing_text_form': writing_text_form,
        'user_input': user_input,
        'answer': answer,
        'memory_buffer': memory.buffer_as_str,
        'memory_load': memory.load_memory_variables({}),
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
