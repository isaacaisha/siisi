# views/chat_forum_views.py

import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils import timezone

from ..models import Room, Topic, Message


@login_required(login_url='login')
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
        'date': timezone.now().strftime(_("%a %d %B %Y")),
        }
    return render(request, 'chat_forum/chat_forum.html', context)


@login_required(login_url='login')
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
        'date': timezone.now().strftime(_("%a %d %B %Y")),
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
            'updated': room.updated.strftime(_('%Y-%m-%d')),
            'created': room.created.strftime(_('%Y-%m-%d')),
            }
        # Print the captured data
        print(_("Room data: {room_data}").format(room_data=json.dumps(room_data, indent=4)))
    return render(request, 'chat_forum/room.html', context)
