from django.contrib.auth.models import User
from home.models import Richiesta_tesi_bozza, Richiesta_prova_finale_bozza, Studente, User, Prova, TesiCreata, Attivita_progettuale_creata
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AttivitaCreataForm(forms.ModelForm):
    class Meta:
        model = Attivita_progettuale_creata
        fields = "__all__"
        exclude = ['author', 'date_posted']

