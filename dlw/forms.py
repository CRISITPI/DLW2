import phonenumbers

from django import forms
from authy.api import AuthyApiClient
from phonenumbers import NumberParseException
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumbers.phonenumberutil import NumberParseException
from django.conf import settings


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']