from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from users.models import Studente, Docente, Profile
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from home.models import Tesi,Attivita_progettuale, Richiesta_tesi, Richiesta_prova_finale
from itertools import chain

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

    all_richiesta_tesi = all_richiesta_pfinale = {}
    nome = request.user.username.split('.')
    for s in all_studenti:
        if s.nome == nome[0] and s.cognome == nome[1] and s.mail == request.user.email:
            all_richiesta_tesi = Richiesta_tesi.objects.filter(autore=s)
            all_richiesta_pfinale = Richiesta_prova_finale.objects.filter(autore=s)
    context_richieste = {
        'all_richiesta_tesi' : all_richiesta_tesi,
        'all_richiesta_pfinale' : all_richiesta_pfinale,
    }

    for doc in all_docenti:
        all_tesi = Tesi.objects.filter(author=request.user)
        all_attivita = Attivita_progettuale.objects.filter(author=request.user)
        tot = list(chain(all_tesi, all_attivita))
        context = {
            'all_tesi': all_tesi,
            'all_attivita': all_attivita,
            # 'tot': tot,
        }
        if doc.mail == request.user.email:
             return render(request, 'users/profile_doc.html', context)

    for stud in all_studenti:
        if stud.mail == request.user.email:
            return render(request, 'users/profile_stud.html', context_richieste)
