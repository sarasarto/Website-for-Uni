from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from users.models import Progetto, Studente, Docente
from .models import Tesi,Attivita_progettuale
from itertools import chain

"""
def index(request):
    context = {
        'projects': Progetto.objects.all(),

    }
    return render(request, 'home/index.html', context)"""


class IndexView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'all_projects'

    def get_queryset(self):
        tesi = Tesi.objects.all()
        a_p = Attivita_progettuale.objects.all()
        tot = list(chain(tesi,a_p))
        return tot


class PostDetailView(DetailView):
    model = Tesi




class TesiCreateView(CreateView):
    model = Tesi
    fields = ['relatore','argomento', 'tirocinio_interno' ,'tirocinio_azienda' , 'data_inizio' , 'data_fine' , 'tag']

    # questo per dire che chi crea
    # la tesi è il docente loggato
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)









"""class LoginView(FormView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {form: 'form'})"""
