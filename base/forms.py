from django import forms

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
    