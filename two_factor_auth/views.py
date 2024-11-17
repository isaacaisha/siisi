from two_factor.views import LoginView

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from .forms import MyUserCreationForm, LoginForm, CustomPasswordResetConfirmForm

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

from django.utils import timezone


class CustomLoginView(LoginView):
    template_name = 'custom_login.html'


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm(request.POST or None)
    hide_navbar = True
    hide_edit_user = True

    if request.method == 'POST':
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'Registration successful! Please finish the setup.')
                # Redirect to two_factor setup
                return redirect('two_factor:setup')
            except Exception as e:
                messages.error(request, f'Sorry, an error occurred: {e}')
        else:
            error_messages = form.errors.as_text()
            messages.error(request, f'Sorry, something went wrong during registration 😝. Details: {error_messages}')

    context = {
        'page': page,
        'form': form,
        'hide_navbar': hide_navbar,
        'hide_edit_user': hide_edit_user,
        'date': timezone.now().strftime("%a %d %B %Y"),
    }
    return render(request, 'two_factor_auth/login_register.html', context)
    
    
def loginPage(request):
    page = 'login'
    form = LoginForm(request.POST or None)
    hide_navbar = True
    hide_edit_user = True

    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email').lower()
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                # Redirect to two_factor login
                return redirect('two_factor:login')
            else:
                messages.error(request, f'User email: {email} or Password  doesn\'t exit 😝')
        else:
            messages.error(request, "Invalid reCAPTCHA. Please try again 😝.")

    context = {
        'page': page,
        'form': form,
        'hide_navbar': hide_navbar,
        'hide_edit_user': hide_edit_user,
        'date': timezone.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'two_factor_auth/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def logoutUserToChat(request):
    logout(request)
    return redirect('chat-forum')


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Password reset email has been sent!')
            return redirect('password_reset_done')
        else:
            messages.error(request, 'Invalid email address.')
    else:
        form = PasswordResetForm()

    context = {
        'form': form,
        'date': timezone.now().strftime("%a %d %B %Y")
    }
    return render(request, 'two_factor_auth/password_reset_request.html', context)

def password_reset_done(request):
    return render(request, 'two_factor_auth/password_reset_done.html')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'two_factor_auth/password_reset_confirm.html'
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = timezone.now().strftime("%a %d %B %Y")
        return context

def password_reset_confirm(request, uidb64, token):
    view = CustomPasswordResetConfirmView.as_view()
    return view(request, uidb64=uidb64, token=token)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'two_factor_auth/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = timezone.now().strftime("%a %d %B %Y")
        return context

def password_reset_complete(request):
    view = CustomPasswordResetCompleteView.as_view()
    return view(request)
