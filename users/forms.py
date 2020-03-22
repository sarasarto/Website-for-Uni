from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    matricola = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'matricola', 'email', 'password1', 'password2']
