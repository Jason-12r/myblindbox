from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(min_length=12, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=12, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'gender', 'weight', 'height', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
