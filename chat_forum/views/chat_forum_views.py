# views/chat_forum_views.py

import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from ..models import Room, Topic, Message
from datetime import datetime


def chatForum(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
        'date': datetime.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'chat_forum/chat_forum.html', context)


@login_required
def room(request, pk):
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
    return render(request, 'chat_forum/room.html', context)
