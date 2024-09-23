# views/utils_gpt_convers.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

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
