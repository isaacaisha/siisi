from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Room, User
from django import forms

# Import ReCaptchaField correctly
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3
from django.contrib.auth.forms import SetPasswordForm

# Create your forms here.

class TextAreaForm(forms.Form):
    writing_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), label='')


class TextAreaDrawingIndex(forms.Form):
    drawing_index = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}), label='')


class ConversationIdForm(forms.Form):
    conversation_id = forms.IntegerField(label='Conversation ID')
    

class DeleteForm(forms.Form):
    conversation_id = forms.IntegerField(label='Conversation ID', required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Conversation ID to delete'
    }))

class DatabaseForm(forms.Form):
    DATABASE_CHOICES = [
        ('Memory', 'Memory'),
        ('User', 'User'),
        ('Theme', 'Theme'),
        ('Message', 'Message'),
        ('MemoryTest', 'MemoryTest'),
        ('BlogPost', 'BlogPost'),
        ('WebsiteReview', 'WebsiteReview'),
        ('DrawingDatabase', 'DrawingDatabase')
    ]
    database_name = forms.ChoiceField(choices=DATABASE_CHOICES, required=True, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    data_id = forms.IntegerField(label='Data ID', required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Data ID to delete'
    }))


class MyUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    class Meta:
        model = User
        fields =  ['name', 'username', 'email', 'password1', 'password2', 'captcha']
        exclude = ['host', 'participants']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'e.g. siisiAi@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    
    # Use reCAPTCHA v2 for login
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class CustomPasswordResetConfirmForm(SetPasswordForm):
    recaptcha = ReCaptchaField()

    def clean_recaptcha(self):
        # Here you can validate the ReCaptcha response if needed
        recaptcha_response = self.cleaned_data.get('recaptcha')

        # Custom validation logic for recaptcha (if required)
        if not recaptcha_response:
            raise forms.ValidationError("ReCAPTCHA validation failed. Please try again.")

        return recaptcha_response


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields =  '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
