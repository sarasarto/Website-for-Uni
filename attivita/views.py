from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views import generic
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy, reverse

from home.views import from_attivitacreata_to_attivitaarchiviata, from_attprogettualecreata_to_richiestaProvabozza
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
    template_name = 'attivita/attivita_progettuale_creata_detail.html'

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
    template_name = 'attivita/attivita_progettuale_creata_form.html'
    fields = ['tutor', 'argomento', 'data_inizio', 'data_fine', 'tag']


def show_attivita(request):
    results = Attivita_progettuale_creata.objects.all().order_by('-date_posted')
    title = "Tutte le attivita progettuali:"
    context = {
        'results': results,
        'title': title,
        'no_results': "Non ci sono attivita progettuali",
    }
    return render(request, 'home/index.html', context)


def show_att_archiviate(request):
    utente = User.objects.get(username=request.user.username)
    docente_log = Docente.objects.get(user=utente)
    results = Attivita_progettuale_Archiviata.objects.filter(author=docente_log).order_by('-data_archiviazione')
    title = "Tutte le attività progettuali archiviate: "

    context = {
        'results': results,
        'title': title,
        'no_results': "Non ci sono attivita progettuali archiviate",
    }
    return render(request, 'home/index.html', context)


class AttivitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Attivita_progettuale_creata
    success_url = '/profile'
    template_name = 'attivita/attivita_progettuale_creata_confirm_delete.html'

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


class AttivitaArchiviataDetailView(DetailView):
    model = Attivita_progettuale_Archiviata
    template_name = 'attivita/attivita_progettuale_creata_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AttivitaArchiviataDetailView, self).get_context_data(**kwargs)
        is_docente = True
        context['is_docente'] = is_docente
        return context


class RequestAttivitaDetailView(FormView, DetailView):
    model = Attivita_progettuale_creata
    template_name = "attivita/precompiled_attivita_request.html"
    form_class = PrecompiledAttivitaRequestForm
    success_url = "/"

    def form_valid(self, form):
        att = self.get_object()
        req = Richiesta_prova_finale_bozza()
        # req.tutor = att.tutor
        # req.argomento = att.argomento
        req.titolo_elaborato = form.cleaned_data.get('titolo_elaborato')
        req.tipologia = form.cleaned_data.get('tipologia')
        req.data_laurea = form.cleaned_data.get('data_laurea')
        from_attprogettualecreata_to_richiestaProvabozza(att, req)

        a = req.tutor

        r = self.request.user.username
        utente = User.objects.get(username=r)
        stud_log = Studente.objects.get(user=utente)
        req.autore = stud_log
        req.modified = False

        """if self.request.user.username != nome:
            messages.error(self.request, f'Autore deve essere lo studente {self.request.user.username}!')
            return redirect('attivita-request-precompiled', pk=self.get_object().id)"""

        all_bozze = Richiesta_prova_finale_bozza.objects.all()
        if all_bozze:
            nome = self.request.user.username.split('.')
            for s in all_bozze:
                if s.autore.nome == nome[0] and s.autore.cognome == nome[1] \
                        and s.autore.mail == self.request.user.email \
                        and s.argomento == req.argomento:
                    messages.error(self.request, f'Esiste già una tua bozza per la attività {req.argomento}!')
                    return redirect('attivita-request-precompiled', pk=self.get_object().id)

        req.save()
        return super().form_valid(form)


class RequestAttivitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Richiesta_prova_finale_bozza
    form_class = RequestProvaFinaleForm
    template_name = "attivita/request_attivita_update.html"
