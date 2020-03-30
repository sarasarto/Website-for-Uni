from django.contrib.auth.models import User
from .models import Richiesta_tesi, Richiesta_prova_finale
from django import forms

"""
class UserForm(forms.ModelForm):

    class Meta:
        module = User
        fields = ['']
"""

class RequestTesiForm(forms.ModelForm):

    class Meta:
        model = Richiesta_tesi
        fields = "__all__"
        # exclude = ['autore']


class RequestProvaFinaleForm(forms.ModelForm):

    class Meta:
        model = Richiesta_prova_finale
        fields = "__all__"


