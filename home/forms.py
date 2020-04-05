from django.contrib.auth.models import User
from .models import Richiesta_tesi, Richiesta_prova_finale , Studente , User
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


class PrecompiledTesiRequestForm(forms.ModelForm):
   """ autore = forms.ModelChoiceField(queryset=Studente.objects.all(),
                                    widget=forms.TextInput,
                                    required=False ,
                                    empty_label=None)"""
    # autore = forms.CharField()
   class Meta:
        model = Richiesta_tesi
        fields = ['autore']



class PrecompiledAttivitaRequestForm(forms.ModelForm):

    class Meta:
        model = Richiesta_prova_finale
        fields = ['autore']
