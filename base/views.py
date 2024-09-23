# base/views.py

import os
import io
import json
import pytz
import numpy as np

from django.shortcuts import get_object_or_404, render, redirect
from django.http import FileResponse, JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .models import Room, ChatData, Topic, Message, User, Conversation
from .forms import TextAreaForm, TextAreaDrawingIndex, RoomForm, UserForm, MyUserCreationForm

from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langdetect import detect
from .utils import find_most_relevant_conversation, generate_conversation_context, handle_llm_response, save_to_database

from datetime import datetime

# Create your views here.

openai = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
llm = ChatOpenAI(temperature=0.0, model="gpt-4o")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)
memory_summary = ConversationSummaryBufferMemory(llm=llm, max_token_limit=3)


@login_required
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


@login_required
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


@login_required
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


@login_required
def latestAudioUrl(request):
    """Provide the URL for the latest audio in user's conversation"""
    latest_conversation = Conversation.objects.filter(owner=request.user).order_by('-created_at').first()

    if latest_conversation and latest_conversation.audio_datas:
        audio_url = reverse('serve_audio_from_db', args=[latest_conversation.id])
        return JsonResponse({"audio_url": audio_url})
    else:
        return JsonResponse({"error": "No audio found"}, status=404)
    

@login_required
def allConversations(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/all_conversations.html', context)
    

@login_required
def likedConversations(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/liked_conversations.html', context)
    

@login_required
def getConversation(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/get_conversation.html', context)
    

@login_required
def deleteConversation(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/delete_conversation.html', context)
    

@login_required
def drawingGenerator(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/drawing_generator.html', context)
    

@login_required
def websiteReviewGenerator(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/website_review_generator.html', context)
    

@login_required
def likedReviews(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/liked_reviews.html', context)
    

@login_required
def extrasFeatures(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/extras_features.html', context)
    
    
def loginPage(request):
    page = 'login'
    hide_navbar = True
    hide_edit_user = True

    if request.user.is_authenticated:
        return redirect('conversation-interface')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, f'User email: {email} doesn\'t exit 😝')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('conversation-interface')
        else:
            messages.error(request, f'User email: {email} or Password  doesn\'t exit 😝')

    context = {
        'page': page,
        'hide_navbar': hide_navbar,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    hide_navbar = True
    hide_edit_user = True

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, f'Sorry, something went wrong during registration 😝')

    context = {
        'page': page,
        'form': form,
        'hide_navbar': hide_navbar,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/login_register.html', context)


@login_required
def chatGpt(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/chat_gpt.html', context)

def response(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')

        # Check if the message was correctly retrieved
        print(f"Message received: {message}")

        completion = openai.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        answer = completion.choices[0].message.content

        # Check the generated answer
        print(f"Answer generated: {answer}")

        new_chat = ChatData(message=message, response=answer)
        
        # Check the ChatData object before saving
        print(f"ChatData to be saved: {new_chat}")

        new_chat.save()

        # Confirm the save operation
        print(f"ChatData saved with id: {new_chat.id}")

        return JsonResponse({'response': answer})
    return JsonResponse({'response': 'Invalid request'}, status=401)


def chatForum(request):
    # Set hide_edit_user to True only if the user is not logged in
    hide_edit_user = not request.user.is_authenticated
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/chat_forum.html', context)


def room(request, pk):
    # Set hide_edit_user to True only if the user is not logged in
    hide_edit_user = not request.user.is_authenticated

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }

    if context:
        # Capture the room's data
        room_data = {
            'id': room.id,
            'host': str(room.host),  # Convert User object to string
            'topic': str(room.topic),  # Convert Topic object to string if it's not a simple type
            'name': room.name,
            'description': room.description,
            # 'participants': room.participants,
            # Format datetime to exclude microseconds and timezone
            'updated': room.updated.strftime('%Y-%m-%d %H:%M:%S'),
            'created': room.created.strftime('%Y-%m-%d %H:%M:%S'),
            }
        # Print the captured data
        print(f"Room data: {json.dumps(room_data, indent=4)}")
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    # Set hide_edit_user to True only if the user is not logged in
    hide_edit_user = request.user.is_authenticated

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    romm_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'romm_messages': romm_messages,
        'topics': topics,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {
        'form': form,
        'topics': topics,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You\'re not Allowed 😝')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {
        'room': room,
        'form': form,
        'topics': topics,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You\'re not Allowed 😝')

    if request.method == 'POST':
        # Capture the room's data before deletion
        room_data = {
            'id': room.id,
            'host': str(room.host),  # Convert User object to string
            'topic': str(room.topic),  # Convert Topic object to string if it's not a simple type
            'name': room.name,
            'description': room.description,
            # 'participants': room.participants,
            # Format datetime to exclude microseconds and timezone
            'updated': room.updated.strftime('%Y-%m-%d %H:%M:%S'),
            'created': room.created.strftime('%Y-%m-%d %H:%M:%S'),
            }
        # Print the captured data
        print(f"Deleted room data: {json.dumps(room_data, indent=4)}")
        # Delete the room
        room.delete()
        return redirect('home')

    context = {
        'obj':room,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }

    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You\'re not Allowed 😝')

    if request.method == 'POST':
        # Delete the message
        message.delete()
        return redirect('home')

    context = {
        'obj':room,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }

    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {
        'form': form,
        'date': datetime.now().strftime("%a %d %B %Y"),
    }
    return render(request, 'base/update_user.html', context)


def topicsPage(request):
    # Set hide_edit_user to True only if the user is not logged in
    hide_edit_user = not request.user.is_authenticated

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)

    context = {
        'topics': topics,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
    }

    return render(request, 'base/topics.html', context)


def activityPage(request):
    # Set hide_edit_user to True only if the user is not logged in
    hide_edit_user = not request.user.is_authenticated
    
    room_messages = Message.objects.all()

    context = {
        'room_messages': room_messages,
        'hide_edit_user': hide_edit_user,
        'date': datetime.now().strftime("%a %d %B %Y"),
    }

    return render(request, 'base/activity.html', context)
