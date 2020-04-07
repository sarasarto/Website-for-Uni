from django.contrib.auth.models import User
from .models import Richiesta_tesi, Richiesta_prova_finale, Studente, User
from django import forms


class RequestTesiForm(forms.ModelForm):
    """ scelte = (
         #("name", User.username),
         ("1" , "sara"),

     )
     autore = forms.MultipleChoiceField(choices=scelte)"""

    class Meta:
        model = Richiesta_tesi
        fields = "__all__"
        # fields = ['autore']


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
