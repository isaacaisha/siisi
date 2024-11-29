# chat_forum/forum.py

from django.forms import ModelForm
from django.utils.translation import gettext as _
from .models import Room, User

# Create your forms here.

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields =  '__all__'
        exclude = ['host', 'participants']
        labels = {
            'name': _('Room Name'),
            'description': _('Room Description'),
            'topic': _('Room Topic'),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
        labels = {
            'avatar': _('Avatar'),
            'name': _('Name'),
            'username': _('Username'),
            'email': _('Email Address'),
            'bio': _('Biography'),
        }
