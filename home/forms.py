from django.contrib.auth.models import User
from .models import Richiesta_tesi, Scelte,Richiesta_prova_finale, Studente, User, Prova
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ScelteForm(forms.ModelForm):
    class Meta:
        model = Scelte
        fields = ['attivita', 'tesi']


class ProvaForm(forms.ModelForm):

    class Meta:
        model = Prova
        fields = "__all__"
        exclude = ['user']


class RequestTesiForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(RequestTesiForm, self).__init__(*args, **kwargs)
    #     self.fields['nome_azienda'].widget = forms.HiddenInput()

    class Meta:
        model = Richiesta_tesi
        fields = "__all__"
        #exclude = ['nome_azienda']
        #fields = ['autore', 'relatore', 'correlatore' , 'argomento' , 'tirocinio_azienda' , 'tirocinio_interno', 'data_laurea']


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
        fields = ['autore', 'data_laurea']


class PrecompiledAttivitaRequestForm(forms.ModelForm):
    class Meta:
        model = Richiesta_prova_finale
        fields = ['autore', 'titolo_elaborato', 'tipologia', 'data_laurea']
