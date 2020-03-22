from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from home.models import Studente, Docente
from .forms import UserRegisterForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_part = username[0:3]
            if first_part.isnumeric():
                s1 = Studente()
                s1.cognome = username
                s1.save()
            else:
                d1 = Docente()
                d1.cognome = username
                d1.save()


            messages.success(request, f'Account created for {username}!')

            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

"""class StudentCreate(CreateView):
    model = Studente
    fields = ['nome', 'cognome', 'matricola', 'mail']"""
