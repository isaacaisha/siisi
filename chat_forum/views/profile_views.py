import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import User, Topic
from ..forms import UserForm
from datetime import datetime


@login_required(login_url='login')
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
    return render(request, 'chat_forum/profile.html', context)


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
    return render(request, 'chat_forum/update_user.html', context)
