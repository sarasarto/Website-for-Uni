from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from users.models import Studente, Docente
from .forms import UserRegisterForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            matricola = form.cleaned_data.get('matricola')

            if matricola.isnumeric():
                sd = Studente()
            else:
                sd = Docente()

            div = username.split('.')
            sd.nome = div[0]
            sd.cognome = div[1]
            sd.matricola = matricola
            sd.mail = form.cleaned_data.get('email')
            sd.save()
            form.save()
            messages.success(request, f'Account created for {username}!')

            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
