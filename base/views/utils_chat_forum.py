# views/utils_chat_forum.py

import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from base.views.chat_forum_views import room

from ..models import Room, Topic, Message
from ..forms import RoomForm

from datetime import datetime


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
        return redirect('topics')

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
        return redirect(f'chat-forum')

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
        return redirect('chat-forum')

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
        return redirect('chat-forum')

    context = {
        'obj':room,
        'message': message,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }

    return render(request, 'base/delete.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)

    context = {
        'topics': topics,
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
