from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from users.models import Progetto


def index(request):
    context = {
        'projects': Progetto.objects.all()
    }
    return render(request, 'home/index.html', context)


class IndexView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'all_projects'

    def get_queryset(self):
        return Progetto.objects.all()


"""class LoginView(FormView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {form: 'form'})"""
