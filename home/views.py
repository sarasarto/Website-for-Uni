from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import generic
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from users.models import Progetto, Studente, Docente
from .models import Tesi, Attivita_progettuale, Richiesta_tesi, Richiesta_prova_finale
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RequestTesiForm, RequestProvaFinaleForm, PrecompiledTesiRequestForm, PrecompiledAttivitaRequestForm
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)


def home(request):
    all_tesi = Tesi.objects.all()
    all_attivita = Attivita_progettuale.objects.all()
    tot = list(chain(all_tesi, all_attivita))
    context = {
        'all_tesi': all_tesi,
        'all_attivita': all_attivita,
        'all_projects': tot
    }
    return render(request, 'home/index.html', context)


"""class IndexView(ListView):
    template_name = 'home/index.html'
    context_object_name = 'all_projects'

    # questo serve per sapere cosa si vedrà nella home
    # sia tesi che attivita progettuale
    def get_queryset(self):
        tesi = Tesi.objects.all()
        a_p = Attivita_progettuale.objects.all()
        tot = list(chain(tesi, a_p))
        return tot"""


def show_tesi(request):
    all_tesi = Tesi.objects.all()
    context = {
        'all_tesi': all_tesi,

    }
    return render(request, 'home/tesi_index.html', context)

def show_attivita(request):
    all_att = Attivita_progettuale.objects.all()
    context = {
        'all_att': all_att,

    }
    return render(request, 'home/attivita_index.html', context)


# TESI
class TesiDetailView(LoginRequiredMixin, DetailView):
    model = Tesi


class TesiCreateView(LoginRequiredMixin, CreateView):
    model = Tesi
    fields = ['relatore', 'argomento', 'tirocinio_interno', 'tirocinio_azienda', 'data_inizio', 'data_fine', 'tag']

    # questo per dire che chi crea
    # la tesi è il docente loggato
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TesiUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tesi
    fields = ['relatore', 'argomento', 'tirocinio_interno', 'tirocinio_azienda', 'data_inizio', 'data_fine', 'tag']

    # questo per dire che chi update
    # la tesi è il docente loggato
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # UserPassesTestMixin serve per controllare che solo
    # chi ha creato il post possa fare update
    def test_func(self):
        tesi = self.get_object()
        if self.request.user == tesi.author:
            return True
        return False


class TesiDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tesi
    success_url = '/profile'

    def test_func(self):
        tesi = self.get_object()
        if self.request.user == tesi.author:
            return True
        return False


# ATTIVITA

class AttivitaDetailView(LoginRequiredMixin, DetailView):
    model = Attivita_progettuale


class AttivitaCreateView(LoginRequiredMixin, CreateView):
    model = Attivita_progettuale
    fields = ['tutor', 'argomento', 'data_inizio', 'data_fine', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AttivitaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Attivita_progettuale
    fields = ['tutor', 'argomento', 'data_inizio', 'data_fine', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # UserPassesTestMixin serve per controllare che solo
    # chi ha creato il post possa fare update
    def test_func(self):
        attivita = self.get_object()
        if self.request.user == attivita.author:
            return True
        return False


class AttivitaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Attivita_progettuale
    success_url = '/profile'

    def test_func(self):
        tesi = self.get_object()
        if self.request.user == tesi.author:
            return True
        return False


# RICHIESTA TESI

def tesi_richiesta(request):
    if request.method == "POST":
        form = RequestTesiForm(request.POST)
        if form.is_valid():
            autore = form.cleaned_data.get('autore')
            nome = autore.nome + '.' + autore.cognome
            if request.user.username != nome:
                messages.error(request, f'Autore deve essere lo studente {request.user.username}!')
                return redirect('tesi-richiesta')
            # req = form.save(commit=False)
            # req.autore = request.user
            form.save()
            messages.success(request, f'La richiesta di {request.user.username} è stata creata correttamente!')
            return redirect('profile')
    else:
        form = RequestTesiForm()
    return render(request, 'home/tesi_request.html', {'form': form})

class RequestTesiDetailView(FormView, DetailView):
    model = Tesi
    template_name = "home/precompiled_tesi_request.html"
    form_class = PrecompiledTesiRequestForm
    success_url = "/"

    def form_valid(self, form):
        tesi = self.get_object()
        req = Richiesta_tesi()
        req.relatore = tesi.relatore
        req.correlatore = tesi.correlatore
        req.argomento = tesi.argomento
        req.tirocinio_interno = tesi.tirocinio_interno
        req.tirocinio_azienda = tesi.tirocinio_azienda
        req.data_inizio = tesi.data_inizio
        req.data_fine = tesi.data_fine
        req.tag = tesi.tag

        req.autore = form.cleaned_data.get('autore')
        req.save()
        return super().form_valid(form)





# RICHIESTA PROVA FINALE

def provafin_richiesta(request):
    if request.method == "POST":
        form = RequestProvaFinaleForm(request.POST)
        if form.is_valid():
            autore = form.cleaned_data.get('autore')
            nome = autore.nome + '.' + autore.cognome
            if request.user.username != nome:
                messages.error(request, f'Autore deve essere lo studente {request.user.username}!')
                return redirect('provafin-richiesta')
            # req = form.save(commit=False)
            # req.autore = request.user
            form.save()
            messages.success(request, f'La richiesta di {request.user.username} è stata creata correttamente!')
            return redirect('profile')
    else:
        form = RequestProvaFinaleForm()
    return render(request, 'home/prova_finale_request.html', {'form': form})


class RequestAttivitaDetailView(FormView, DetailView):
    model = Attivita_progettuale
    template_name = "home/precompiled_attivita_request.html"
    form_class = PrecompiledAttivitaRequestForm
    success_url = "/"

    def form_valid(self, form):
        att = self.get_object()
        req = Richiesta_prova_finale()
        req.tutor = att.tutor
        req.argomento = att.argomento
        req.data_inizio = att.data_inizio
        req.data_fine = att.data_fine
        req.tag = att.tag

        req.autore = form.cleaned_data.get('autore')
        req.save()
        return super().form_valid(form)
