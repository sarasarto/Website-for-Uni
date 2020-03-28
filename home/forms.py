from django.contrib.auth.models import User
from .models import Richiesta_tesi
from django import forms

"""
class UserForm(forms.ModelForm):

    class Meta:
        module = User
        fields = ['']
"""

class RequestForm(forms.ModelForm):

    class Meta:
        model = Richiesta_tesi
        fields = "__all__"
        # exclude = ['autore']


