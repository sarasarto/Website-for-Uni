from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import generic
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from users.models import Studente, Docente
from .models import Tesi, Attivita_progettuale, Richiesta_tesi, Richiesta_tesi_inviata, Richiesta_prova_finale, User
from users.models import Studente, Docente
from .models import Tesi, Attivita_progettuale, TesiArchiviata, Attivita_progettuale_Archiviata
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RequestTesiForm, RequestProvaFinaleForm, PrecompiledTesiRequestForm, PrecompiledAttivitaRequestForm
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.conf import settings
from django.template.loader import get_template


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


def show_tesi_archiviate(request):
    all_tesi = TesiArchiviata.objects.filter(author=request.user)

    context = {
        'all_tesi': all_tesi,

    }
    return render(request, 'home/archivio_tesi.html', context)


def show_att_archiviate(request):
    all_att = Attivita_progettuale_Archiviata.objects.filter(author=request.user)

    context = {
        'all_att': all_att,

    }
    return render(request, 'home/archivio_attivita.html', context)


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

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        # modo stupido di farlo - ma funziona
        ta = TesiArchiviata()
        ta.author = self.object.author
        ta.relatore = self.object.relatore
        ta.argomento = self.object.argomento
        ta.correlatore = self.object.correlatore
        ta.data_fine = self.object.data_fine
        ta.data_inizio = self.object.data_inizio
        ta.tirocinio_azienda = self.object.tirocinio_azienda
        ta.tirocinio_interno = self.object.tirocinio_interno
        ta.tag = self.object.tirocinio_interno
        ta.save()
        self.object.delete()
        return redirect('profile')


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

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        # modo stupido di farlo - ma funziona
        ta = Attivita_progettuale_Archiviata()
        ta.author = self.object.author
        ta.tutor = self.object.tutor
        ta.argomento = self.object.argomento

        ta.data_fine = self.object.data_fine
        ta.data_inizio = self.object.data_inizio
        ta.tag = self.object.tag
        ta.save()
        self.object.delete()
        return redirect('profile')


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


class RichiestaTesiInviateListView(ListView):
    model = Richiesta_tesi_inviata
    template_name='home/richiesta_tesi_inviata.html'
    context_object_name = 'all_richiesta_tesi'


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

        nome = req.autore.nome + '.' + req.autore.cognome
        if self.request.user.username != nome:
            messages.error(self.request, f'Autore deve essere lo studente {self.request.user.username}!')
            return redirect('tesi-request-precompiled', pk=self.get_object().id)
        req.save()
        return super().form_valid(form)


class RTDetailView(DetailView):
    model = Richiesta_tesi

    def get(self, request, pk):
        rel = self.get_object().relatore
        doc = rel.split()
        doc_mail = doc[1]

        author = self.get_object().autore
        stud_name = author.nome
        stud_surname = author.cognome

        rti = Richiesta_tesi_inviata()
        r = self.get_object()
        rti.relatore = r.relatore
        rti.correlatore = r.correlatore
        rti.argomento = r.argomento
        rti.tirocinio_interno = r.tirocinio_interno
        rti.tirocinio_azienda = r.tirocinio_azienda
        rti.data_inizio = r.data_inizio
        rti.data_fine = r.data_fine
        rti.tag = r.tag
        rti.autore = r.autore
        rti.save()

        if request.GET.get('Send') == 'Send':
            subject = 'Richiesta Tesi'
            from_email = settings.EMAIL_HOST_USER
            to_email = [doc_mail]
            message = EmailMultiAlternatives(subject=subject,
                                             from_email=from_email,
                                             to=to_email,
                                             )
            context = {
                'name': stud_name,
                'surname': stud_surname,
                'matricola': author.matricola,
                'mail': author.mail,
                'inizio': rti.data_inizio,
                'argomento': rti.argomento,
                'id': rti.id,
            }
            r.delete()
            html_template = get_template('home/richiesta_email.html').render(context)
            message.attach_alternative(html_template, "text/html")
            message.send()

            messages.success(request, f'La mail è stata inviata correttamente al seguente indirizzo {doc_mail}!')
            return redirect('profile')

        else:
            rti.delete()
            return super().get(request, pk)


"""@login_required
def accetta_rifiuta(self, request, pk):
    context = {
        'name': request.user.username

    }
    return render(request, 'home/accept.html', context)"""


class AccettaRifiutaDetailView(LoginRequiredMixin, DetailView):
    model = Richiesta_tesi_inviata
    template_name = "home/accept.html"
    success_url = '/'

    def get(self, request, pk):
        success_url = '/'
        self.object = self.get_object()
        context = {
            'name': self.object.autore,
            'argomento': self.object.argomento,
            'mail': self.object.autore.mail,
            'inizio': self.get_object().data_inizio,
            'argomento': self.get_object().argomento,

        }

        if request.GET.get('Accetta') == 'Accetta':
            rel = self.get_object().relatore
            doc = rel.split()
            doc_name = doc[0]
            doc_mail = doc[1]
            author = self.get_object().autore
            stud_name = author.nome
            stud_surname = author.cognome
            subject = 'Accettata la Richiesta Tesi'
            from_email = settings.EMAIL_HOST_USER
            to_email = [self.object.autore.mail]
            message = EmailMultiAlternatives(subject=subject,
                                             from_email=from_email,
                                             to=to_email,
                                             )
            context = {
                'nome':stud_name,
                'cognome':stud_surname,
                'prof': doc_name,
                'argomento': self.get_object().argomento,
                'mail': doc_mail

            }
            html_template = get_template('home/accetta_email.html').render(context)
            message.attach_alternative(html_template, "text/html")
            message.send()
            messages.success(request, f'La mail è stata inviata correttamente al seguente indirizzo {self.object.autore.mail}!')
            return super().get(request, pk)
        else:
            if request.GET.get('Rifiuta') == 'Rifiuta':
                rel = self.get_object().relatore
                doc = rel.split()
                doc_name = doc[0]
                doc_mail = doc[1]
                author = self.get_object().autore
                stud_name = author.nome
                stud_surname = author.cognome
                subject = 'Rifiutata la Richiesta Tesi'
                from_email = settings.EMAIL_HOST_USER
                to_email = [self.object.autore.mail]
                message = EmailMultiAlternatives(subject=subject,
                                                 from_email=from_email,
                                                 to=to_email,
                                                 )
                context = {
                    'nome': stud_name,
                    'cognome': stud_surname,
                    'prof': doc_name,
                    'argomento': self.get_object().argomento,
                    'mail': doc_mail

                }
                html_template = get_template('home/rifiuto_email.html').render(context)
                message.attach_alternative(html_template, "text/html")
                message.send()
                messages.success(request,
                                 f'La mail è stata inviata correttamente al seguente indirizzo {self.object.autore.mail}!')
                return super().get(request, pk)
            else:
                rt = Richiesta_tesi()
                r = self.get_object()
                rt.relatore = r.relatore
                rt.correlatore = r.correlatore
                rt.argomento = r.argomento
                rt.tirocinio_interno = r.tirocinio_interno
                rt.tirocinio_azienda = r.tirocinio_azienda
                rt.data_inizio = r.data_inizio
                rt.data_fine = r.data_fine
                rt.tag = r.tag
                rt.autore = r.autore
                rt.save()

                if request.GET.get('Segnala Errori') == 'Segnala Errori':
                    rel = self.get_object().relatore
                    doc = rel.split()
                    doc_name = doc[0]
                    doc_mail = doc[1]
                    author = self.get_object().autore
                    stud_name = author.nome
                    stud_surname = author.cognome
                    subject = 'Errori nella Richiesta Tesi'
                    from_email = settings.EMAIL_HOST_USER
                    to_email = [self.object.autore.mail]

                    message = EmailMultiAlternatives(subject=subject,
                                                     from_email=from_email,
                                                     to=to_email,
                                                     )
                    context = {
                        'nome': stud_name,
                        'cognome': stud_surname,
                        'prof': doc_name,
                        'argomento': rt.argomento,
                        'mail': doc_mail

                    }
                    r.delete()
                    html_template = get_template('home/errore_email.html').render(context)
                    message.attach_alternative(html_template, "text/html")
                    message.send()
                    messages.success(request,
                                     f'La mail è stata inviata correttamente al seguente indirizzo {self.object.autore.mail}!')
                    return redirect("/")
                else:
                    rt.delete()
                    return super().get(request, pk)


        return self.render_to_response(context)
    # controllare che chi si logga sia il relatore -- non funziona
    def test_func(self):
        richiesta = self.get_object()
        nome = richiesta.relatore.split()
        if self.request.user.username == nome[0]:
            return True
        return False




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
        nome = req.autore.nome + '.' + req.autore.cognome
        if self.request.user.username != nome:
            messages.error(self.request, f'Autore deve essere lo studente {self.request.user.username}!')
            return redirect('attivita-request-precompiled', pk=self.get_object().id)
        req.save()
        return super().form_valid(form)


class RAPDetailView(DetailView):
    model = Richiesta_prova_finale

    def get(self, request, pk):
        rel = self.get_object().tutor
        # print(rel)
        doc = rel.split()
        doc_mail = doc[1]
        print(doc_mail)
        if request.GET.get('Send') == 'Send':
            send_mail('provaTesi', 'stiamo provando', settings.EMAIL_HOST_USER, [doc_mail], fail_silently=False)
            messages.success(request, f'La mail è stata inviata correttamente al seguente indirizzo {doc_mail}!')
        return super().get(request, pk)
