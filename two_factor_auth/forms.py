# two_factor_auth/form.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

# Import ReCaptchaField correctly
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox # , ReCaptchaV3

from django.contrib.auth.forms import SetPasswordForm

from .models import User

# Create your forms here.

class MyUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    captcha.label = _('Captcha')
    
    class Meta:
        model = User
        fields =  ['name', 'username', 'email', 'password1', 'password2', 'captcha']
        exclude = ['host', 'participants']

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        # Add translations for the form labels
        self.fields['name'].label = _('Name')
        self.fields['username'].label = _('Username')
        self.fields['email'].label = _('Email')
        self.fields['password1'].label = _('Password')
        self.fields['password2'].label = _('Confirm Password')
        self.fields['captcha'].label = _('Captcha')


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': _('e.g. siisiChacal@gmail.com')}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('••••••••')}))
    
    # Use reCAPTCHA v2 for login
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    captcha.label = _('Captcha')


class CustomPasswordResetConfirmForm(SetPasswordForm):
    recaptcha = ReCaptchaField()

    def clean_recaptcha(self):
        # Here you can validate the ReCaptcha response if needed
        recaptcha_response = self.cleaned_data.get('recaptcha')

        # Custom validation logic for recaptcha (if required)
        if not recaptcha_response:
            raise forms.ValidationError(_("ReCAPTCHA validation failed. Please try again."))

        return recaptcha_response
