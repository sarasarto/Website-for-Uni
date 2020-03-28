from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from users.models import Progetto, Studente, Docente
from .models import Tesi, Attivita_progettuale
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RequestForm


class IndexView(ListView):
    template_name = 'home/index.html'
    context_object_name = 'all_projects'

    # questo serve per sapere cosa si vedrà nella home
    # sia tesi che attivita progettuale
    def get_queryset(self):
        tesi = Tesi.objects.all()
        a_p = Attivita_progettuale.objects.all()
        tot = list(chain(tesi, a_p))
        return tot


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Tesi


class TesiCreateView(CreateView):
    model = Tesi
    fields = ['relatore', 'argomento', 'tirocinio_interno', 'tirocinio_azienda', 'data_inizio', 'data_fine', 'tag']

    # questo per dire che chi crea
    # la tesi è il docente loggato
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def tesi_richiesta(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
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
        form = RequestForm()
    return render(request, 'home/tesi_request.html', {'form': form})
