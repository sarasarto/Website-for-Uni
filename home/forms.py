from django.contrib.auth.models import User
from .models import Richiesta_tesi_bozza, Richiesta_prova_finale_bozza, Studente, User, Prova, TesiCreata, Attivita_progettuale_creata
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ScelteForm(forms.Form):
    solo_attivita = forms.BooleanField(required=False)
    solo_tesi = forms.BooleanField(required=False)


class TesiCreataForm(forms.ModelForm):
    class Meta:
        model = TesiCreata
        fields = "__all__"
        exclude = ['author', 'date_posted']


class AttivitaCreataForm(forms.ModelForm):
    class Meta:
        model = Attivita_progettuale_creata
        fields = "__all__"
        exclude = ['author', 'date_posted']


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
        model = Richiesta_tesi_bozza
        fields = "__all__"
        exclude = ['date_posted', 'autore']
        # fields = ['autore', 'relatore', 'correlatore' , 'argomento' , 'tirocinio_azienda' , 'tirocinio_interno', 'data_laurea']


class RequestProvaFinaleForm(forms.ModelForm):
    class Meta:
        model = Richiesta_prova_finale_bozza
        fields = "__all__"
        exclude = ['date_posted', 'autore']


class PrecompiledTesiRequestForm(forms.ModelForm):

    #autore = forms.CharField(initial="nome.cognome")
    class Meta:
        model = Richiesta_tesi_bozza
        fields = ['data_laurea']



class PrecompiledAttivitaRequestForm(forms.ModelForm):
    class Meta:
        model = Richiesta_prova_finale_bozza
        fields = [ 'titolo_elaborato', 'tipologia', 'data_laurea']
