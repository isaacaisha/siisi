import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ..forms import MyUserCreationForm
from ..models import User
from datetime import datetime
    
    
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

def logoutUserToChat(request):
    logout(request)
    return redirect('chat-forum')


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
            return redirect('conversation-interface')
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
