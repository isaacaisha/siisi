# base/forms.py

from django import forms
from django.utils.translation import gettext as _

# Create your forms here.

class TextAreaForm(forms.Form):
    writing_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), label=_('Writing Text'))


class TextAreaDrawingIndex(forms.Form):
    drawing_index = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}), label=_('Drawing Index'))


class ConversationIdForm(forms.Form):
    conversation_id = forms.IntegerField(label=_('Conversation ID'))
    

class DeleteForm(forms.Form):
    conversation_id = forms.IntegerField(label=_('Conversation ID'), required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': _('Enter Conversation ID to delete')
    }))
