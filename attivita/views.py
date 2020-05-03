from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views import generic
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy, reverse

from home.views import from_attivitacreata_to_attivitaarchiviata
from tesi import settings
from users.models import Studente, Docente
from home.models import TesiCreata, Attivita_progettuale_creata, Richiesta_tesi_bozza, Richiesta_tesi_inviata, \
    Richiesta_prova_finale_bozza, User, \
    Richiesta_prova_finale_inviata
from users.models import Studente, Docente
from home.models import TaggableManager, TesiArchiviata, Attivita_progettuale_Archiviata, Prova
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from home.forms import RequestTesiForm, RequestProvaFinaleForm, PrecompiledTesiRequestForm, \
    PrecompiledAttivitaRequestForm, \
    ProvaForm, ScelteForm, TesiCreataForm
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from .forms import AttivitaCreataForm
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage

from django.template.loader import get_template
from django.db.models import Q
from itertools import chain


class AttivitaDetailView(LoginRequiredMixin, DetailView):
    model = Attivita_progettuale_creata

    def get_context_data(self, **kwargs):
        context = super(AttivitaDetailView, self).get_context_data(**kwargs)
        is_docente = False
        all_docenti = Docente.objects.all()
        # now = self.request.user
        nome = self.request.user.username.split('.')
        for doc in all_docenti:
            d_nome = doc.nome
            if doc.nome == nome[0] and doc.cognome == nome[1] and doc.mail == self.request.user.email:
                is_docente = True

        context['is_docente'] = is_docente
        return context


def AttivitaCreate(request):
    r = request.user.username
    if request.method == "POST":
        form = AttivitaCreataForm(request.POST)
        if form.is_valid():
            att_create = form.save(commit=False)

            utente = User.objects.get(username=r)
            docente_log = Docente.objects.get(user=utente)
            att_create.author = docente_log
            # form.fields['author'] = docente_log
            # p.save()

            att_create.save()
            form.save_m2m()
            messages.success(request, f'La attività di {request.user.username} è stata creata correttamente!')
            return redirect('profile')
    else:
        form = AttivitaCreataForm(initial={'tutor': r})

    return render(request, 'attivita/attivita_progettuale_creata_form.html', {'form': form})


class AttivitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Attivita_progettuale_creata
    fields = ['tutor', 'argomento', 'data_inizio', 'data_fine', 'tag']


class AttivitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Attivita_progettuale_creata
    success_url = '/profile'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        # modo stupido di farlo - ma funziona
        ta = Attivita_progettuale_Archiviata()
        # ta.author = self.object.author
        # ta.tutor = self.object.tutor
        # ta.argomento = self.object.argomento

        # ta.data_fine = self.object.data_fine
        # ta.data_inizio = self.object.data_inizio
        # ta.tag = self.object.tag
        # ta.save()
        # self.object.delete()
        from_attivitacreata_to_attivitaarchiviata(self.object, ta)
        return redirect('profile')
