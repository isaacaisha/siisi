from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 
from .models import Room, User
from django import forms

# Create your forms here.

class TextAreaForm(forms.Form):
    writing_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), label='')

class TextAreaDrawingIndex(forms.Form):
    drawing_index = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}), label='')


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields =  ['name', 'username', 'email', 'password1', 'password2']
        exclude = ['host', 'participants']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields =  '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
