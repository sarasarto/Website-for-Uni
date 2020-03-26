from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from users.models import Studente, Docente, Profile
from .forms import UserRegisterForm
from django.contrib.auth.models import User


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
    all_docenti = Docente.objects.all()
    all_studenti = Studente.objects.all()

    cont = True
    for doc in all_docenti:
        if doc.mail == request.user.email:
            cont = False
            return render(request, 'users/profile_doc.html')

    if cont:
        for stud in all_studenti:
            if stud.mail == request.user.email:
                return render(request, 'users/profile_stud.html')
