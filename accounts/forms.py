from django.contrib.auth import (authenticate, get_user_model)
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.conf import settings
import requests
from django import forms


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(min_length=6, max_length=100, label=u'Password', required=True)

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','password1', 'password2', )

class PasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
