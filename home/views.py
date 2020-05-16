from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotModified
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views import generic
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy, reverse
from tesi import settings
from users.models import Studente, Docente
from .models import TesiCreata, Attivita_progettuale_creata, Richiesta_tesi_bozza, Richiesta_tesi_inviata, \
    Richiesta_prova_finale_bozza, User, \
    Richiesta_prova_finale_inviata
from users.models import Studente, Docente
from .models import TaggableManager, TesiArchiviata, Attivita_progettuale_Archiviata, Prova
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RequestTesiForm, RequestProvaFinaleForm, PrecompiledTesiRequestForm, PrecompiledAttivitaRequestForm, \
    ProvaForm, ScelteForm, TesiCreataForm
from attivita.forms import  AttivitaCreataForm
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage

from django.template.loader import get_template
from django.db.models import Q
from itertools import chain

"""def home(request):
    all_tesi = Tesi.objects.all()
    all_attivita = Attivita_progettuale.objects.all()
    tot = list(chain(all_tesi, all_attivita))
    context = {
        'all_tesi': all_tesi,
        'all_attivita': all_attivita,
        'all_projects': tot
    }
    return render(request, 'home/index.html', context)"""


class IndexView(ListView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        all_tesi = TesiCreata.objects.all()
        all_attivita = Attivita_progettuale_creata.objects.all()
        tot = list(chain(all_tesi, all_attivita))
        tot = sorted(tot, key=lambda x: x.date_posted, reverse=True)
        context = {
            'all_tesi': all_tesi,
            'all_attivita': all_attivita,
            'results': tot
        }
        return context

    def get_queryset(self):
        tesi = TesiCreata.objects.all()
        a_p = Attivita_progettuale_creata.objects.all()
        tot = list(chain(tesi, a_p))
        return tot


"""class SearchIndexView(ListView):
    template_name = 'home/cerca.html'
    all_tesi = Tesi.objects.all()
    all_att = Attivita_progettuale.objects.all()
    context = {
        'all_tesi': all_tesi,
        'all_att': all_att
    }

    def get_queryset(query=None):
        queryset = []
        queries = query.split(" ")
        for q in queries:
            tesi = Tesi.objects.filter(tag=q).distinct
            # a_p = Attivita_progettuale.objects.all()
            # tot = list(chain(tesi, a_p))

            for post in tesi:
                queryset.append(post)

        return list(set(queryset))"""


def prova(request):
    r = request.user.username
    if request.method == "POST":
        form = ProvaForm(request.POST)
        if form.is_valid():
            p = Prova()
            nome = form.cleaned_data.get('nome')
            p.nome = nome

            p.user = User.objects.get(username=nome)

            p.save()
            # form.save()
            messages.success(request, f'La richiesta di {request.user.username} è stata creata correttamente!')
            return redirect('profile')
    else:
        form = ProvaForm(initial={'nome': r})

    return render(request, 'home/prova.html', {'form': form})


def cerca(request):
    template = 'home/cerca.html'
    query = request.GET.get('q')  # la variabile per le query
    lista_q = query.split(" ")
    results = []
    risultati_tutti = []
    attivita_tutte = []
    title = "Risultati della ricerca per " + "'" + query + "'" + " :"

    for p in lista_q:
        risultati = TesiCreata.objects.filter(Q(argomento__icontains=p) |
                                              Q(tag__name=p)
                                              ).distinct()
        att = Attivita_progettuale_creata.objects.filter(Q(argomento__icontains=p) |
                                                         Q(tag__name=p)
                                                         ).distinct()
        risultati_tutti = list(chain(risultati_tutti, risultati))
        attivita_tutte = list(chain(attivita_tutte, att))
        results = list(chain(risultati, results, att))

    if request.method == "POST":
        form = ScelteForm(request.POST)
        if form.is_valid():

            att_form = form.cleaned_data.get('solo_attivita')
            tesi_form = form.cleaned_data.get('solo_tesi')

            if att_form:
                attivita_tutte = sorted(attivita_tutte, key=lambda x: x.date_posted, reverse=True)
                attivita_tutte = list(set(attivita_tutte))  # per togliere duplicati
                results = attivita_tutte

                context = {
                    'query': query,
                    'results': results,
                    'form': form,
                    'title': title,
                }
                return render(request, template, context)
            if tesi_form:
                risultati_tutti = sorted(risultati_tutti, key=lambda x: x.date_posted, reverse=True)
                risultati_tutti = list(set(risultati_tutti))  # per togliere duplicati
                results = risultati_tutti

                context = {
                    'query': query,
                    'results': results,
                    'form': form,
                    'title': title,
                }
                return render(request, template, context)

    else:
        form = ScelteForm()

    results = sorted(results, key=lambda x: x.date_posted, reverse=True)
    results = list(set(results))  # per togliere duplicati

    context = {
        'query': query,
        'results': results,
        'form': form,
        'att': attivita_tutte,
        'risultati': risultati_tutti,
        'title': title,
    }
    return render(request, template, context)


def show_tesi(request):
    # all_tesi = TesiCreata.objects.all().order_by('-date_posted')
    results = TesiCreata.objects.all().order_by('-date_posted')
    title = "Tutte le tesi:"
    context = {
        'results': results,
        'title': title,
        'no_results': "Non ci sono tesi"

    }
    return render(request, 'home/index.html', context)


class TesiArchiviataDetailView(DetailView):
    model = TesiArchiviata
    template_name = 'home/tesicreata_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TesiArchiviataDetailView, self).get_context_data(**kwargs)
        is_docente = True
        context['is_docente'] = is_docente
        return context


def show_tesi_archiviate(request):
    utente = User.objects.get(username=request.user.username)
    docente_log = Docente.objects.get(user=utente)
    results = TesiArchiviata.objects.filter(author=docente_log).order_by('-data_archiviazione')
    title = "Tutte le tesi archiviate:"

    context = {
        'results': results,
        'title': title,
        'no_results': "Non ci sono tesi archiviate"
    }
    return render(request, 'home/index.html', context)

# TESI


class TesiDetailView(LoginRequiredMixin, DetailView):
    model = TesiCreata
    # template_name = 'home/tesicreata_detail.html'
    template_name = 'home/detail_tesi_creata_template.html'

    def get_context_data(self, **kwargs):
        context = super(TesiDetailView, self).get_context_data(**kwargs)
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


def TesiCreate(request):
    r = request.user.username
    if request.method == "POST":
        form = TesiCreataForm(request.POST)
        if form.is_valid():
            tesi_create = form.save(commit=False)

            utente = User.objects.get(username=r)
            docente_log = Docente.objects.get(user=utente)
            tesi_create.author = docente_log

            tesi_create.save()
            form.save_m2m()
            messages.success(request, f'La tesi di {request.user.username} è stata creata correttamente!')
            return redirect('profile')
    else:
        form = TesiCreataForm(initial={'relatore': r})

    return render(request, 'home/tesicreata_form.html', {'form': form})


"""class TesiCreateView(LoginRequiredMixin, CreateView):
    model = TesiCreata
    fields = ['relatore', 'argomento', 'tirocinio', 'nome_azienda', 'data_inizio', 'data_fine', 'tag']

    # questo per dire che chi crea
    # la tesi è il docente loggato
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)"""


class TesiUpdateView(LoginRequiredMixin, UpdateView):
    model = TesiCreata
    fields = ['relatore', 'argomento', 'tirocinio', 'nome_azienda', 'data_inizio', 'data_fine', 'tag']




class TesiDeleteView(LoginRequiredMixin, DeleteView):
    model = TesiCreata
    success_url = '/profile'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        # modo stupido di farlo - ma funziona
        ta = TesiArchiviata()
        from_tesicreata_to_tesiarchiviata(self.object, ta)
        # ta.author = self.object.author
        # ta.relatore = self.object.relatore
        # ta.argomento = self.object.argomento
        # ta.correlatore = self.object.correlatore
        # ta.data_fine = self.object.data_fine
        # ta.data_inizio = self.object.data_inizio
        # ta.tirocinio = self.object.tirocinio
        # ta.nome_azienda = self.object.nome_azienda
        # ta.tag = self.object.tag
        # ta.save()
        # self.object.delete()
        return redirect('profile')


# ATTIVITA

"""class AttivitaCreateView(LoginRequiredMixin, CreateView):
    model = Attivita_progettuale_creata
    fields = ['tutor', 'argomento', 'data_inizio', 'data_fine', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
"""






# RICHIESTA TESI


def tesi_richiesta(request):
    if request.method == "POST":
        form = RequestTesiForm(request.POST)
        if form.is_valid():
            r = request.user.username
            richiesta_create = form.save(commit=False)
            utente = User.objects.get(username=r)
            studente_log = Studente.objects.get(user=utente)
            richiesta_create.autore = studente_log

            if r != str(studente_log):
                messages.error(request, f'Autore deve essere lo studente {request.user.username}!')
                return redirect('tesi-richiesta')

            richiesta_create.save()
            messages.success(request, f'La richiesta di {request.user.username} è stata creata correttamente!')
            return redirect('profile')
    else:
        form = RequestTesiForm()
    return render(request, 'home/tesi_request.html', {'form': form})


def RichiestaTesiInviate(request):
    # nome = request.user.username.split('.')
    all_studenti = Studente.objects.all()
    results = {}
    nome = request.user.username.split('.')
    for s in all_studenti:
        if s.nome == nome[0] and s.cognome == nome[1] and s.mail == request.user.email:
            results = Richiesta_tesi_inviata.objects.filter(autore=s).order_by('-date_posted')


    context = {
        #'all_richiesta_tesi': all_richiesta_tesi,
        'results': results,
        'title': "Le tue tesi inviate: ",
        'no_results': "Non hai ancora inviato nessuna tesi"
    }
    return render(request, 'home/index.html', context)


class RequestTesiDetailView(FormView, DetailView):
    model = TesiCreata
    template_name = "home/precompiled_tesi_request.html"
    form_class = PrecompiledTesiRequestForm
    success_url = "/"

    def form_valid(self, form):
        tesi = self.get_object()
        req = Richiesta_tesi_bozza()
        # req.relatore = tesi.relatore
        # req.correlatore = tesi.correlatore
        # req.argomento = tesi.argomento
        # req.tirocinio = tesi.tirocinio
        # req.nome_azienda = tesi.nome_azienda
        # req.data_inizio = tesi.data_inizio
        # req.data_fine = tesi.data_fine
        # req.tag = tesi.tag
        from_tesicreata_to_richiestabozza(tesi, req)
        req.modified = False
        req.data_laurea = form.cleaned_data.get('data_laurea')

        #req.autore = form.cleaned_data.get('autore')
        a = req.relatore
        r = self.request.user.username
        utente = User.objects.get(username=r)
        stud_log = Studente.objects.get(user=utente)
        req.autore = stud_log
        #nome = req.autore.nome + '.' + req.autore.cognome
        """if self.request.user.username != nome:
            messages.error(self.request, f'Autore deve essere lo studente {self.request.user.username}!')
            return redirect('tesi-request-precompiled', pk=self.get_object().id)"""

        all_bozze = Richiesta_tesi_bozza.objects.all()
        nome = self.request.user.username.split('.')
        for s in all_bozze:
            if s.autore.nome == nome[0] and s.autore.cognome == nome[1] and \
                    s.autore.mail == self.request.user.email and \
                    s.argomento == req.argomento:
                messages.error(self.request, f'Esiste già una tua bozza per la tesi {req.argomento}!')
                return redirect('tesi-request-precompiled', pk=self.get_object().id)

        req.save()
        return super().form_valid(form)


def RequestTesiDetail(request):
    r = request.user.username
    if request.method == "POST":
        form = PrecompiledTesiRequestForm(request.POST)
        if form.is_valid():

            richiesta_create = form.save(commit=False)
            utente = User.objects.get(username=r)
            studente_log = Studente.objects.get(user=utente)
            richiesta_create.autore = studente_log

            if r != str(studente_log):
                messages.error(request, f'Autore deve essere lo studente {request.user.username}!')
                return redirect('tesi-richiesta')

            richiesta_create.save()
            messages.success(request, f'La richiesta di {request.user.username} è stata creata correttamente!')
            return redirect('profile')
    else:
        form = PrecompiledTesiRequestForm(initial={'autore': r})
    return render(request, 'home/precompiled_tesi_request.html', {'form': form})


class RequestTesiUpdateView(LoginRequiredMixin, UpdateView):
    model = Richiesta_tesi_bozza
    form_class = RequestTesiForm
    template_name = "home/request_tesi_update.html"
    # fields = "__all__"

    # def form_valid(self, form):
    #     form.instance.author = self.request.username
    #     return super().form_valid(form)


class RequestTesiDeleteView(LoginRequiredMixin, DeleteView):
    model = Richiesta_tesi_bozza
    success_url = '/profile'


class RTDetailView(DetailView):
    model = Richiesta_tesi_bozza
    template_name = 'home/detail_richiesta_tesi_template.html'

    def get(self, request, pk):
        rel = self.get_object().relatore
        # doc = rel.split()
        # doc_mail = doc[1]
        doc_mail = rel.mail
        author = self.get_object().autore
        stud_name = author.nome
        stud_surname = author.cognome

        rti = Richiesta_tesi_inviata()
        r = self.get_object()
        from_richiestatesibozza_to_richiestatesiinviata(r, rti)
        # rti.relatore = r.relatore
        # rti.correlatore = r.correlatore
        # rti.argomento = r.argomento
        # rti.tirocinio = r.tirocinio
        # rti.nome_azienda = r.nome_azienda

        # rti.autore = r.autore
        # rti.data_laurea = r.data_laurea
        # rti.save()

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
                'laurea': rti.data_laurea,
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


class AccettaRifiutaTesiDetailView(LoginRequiredMixin, DetailView):
    model = Richiesta_tesi_inviata
    template_name = "home/accept.html"
    success_url = '/'

    def get(self, request, pk):
        log = self.request.user.username
        log = log.split('.')
        self.object = self.get_object()
        rel_n = self.object.relatore.nome
        rel_c = self.object.relatore.cognome
        # rt = self.object.banama
        if log[0] != rel_n or log[1] != rel_c:
            # messages.error(request, f'Errore! si puo loggare solo il docente tutor')
            return redirect('/login/?next=/' + str(self.get_object().id) + '/accept_tesi')
        else:
            self.object = self.get_object()
            autore = self.object.autore
            context_object_name = {
                'name': self.object.autore,
                'argomento': self.object.argomento,
                'mail': self.object.autore.mail,
                'data': self.object.data_laurea,
            }
            if request.GET.get('Accetta') == 'Accetta':
                rel = self.get_object().relatore
                # doc = rel.split()
                # doc_name = doc[0]
                # doc_mail = doc[1]
                doc_name = rel.nome + ' ' + rel.cognome
                doc_mail = rel.mail
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
                    'nome': stud_name,
                    'cognome': stud_surname,
                    'prof': doc_name,
                    'argomento': self.get_object().argomento,
                    'mail': doc_mail

                }
                html_template = get_template('home/accetta_email.html').render(context)
                message.attach_alternative(html_template, "text/html")
                message.send()
                messages.success(request,
                                 f'La mail è stata inviata correttamente al seguente indirizzo {self.object.autore.mail}!')
                return redirect("/")
            else:
                if request.GET.get('Rifiuta') == 'Rifiuta':
                    rel = self.get_object().relatore
                    # doc = rel.split()
                    # doc_name = doc[0]
                    # doc_mail = doc[1]
                    doc_name = rel.nome + ' ' + rel.cognome
                    doc_mail = rel.mail
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
                    self.get_object().delete()
                    return redirect("/")
                else:
                    # se c'è errore allora
                    # rimette la tesi in richiesta tesi
                    rt = Richiesta_tesi_bozza()
                    r = self.get_object()
                    from_richiestatesiinviata_to_richiestatesibozza(r, rt)
                    # rt.relatore = r.relatore
                    # rt.correlatore = r.correlatore
                    # rt.argomento = r.argomento
                    # rt.tirocinio = r.tirocinio
                    # rt.nome_azienda = r.nome_azienda
                    # rt.data_laurea = r.data_laurea
                    # rt.autore = r.autore
                    # rt.save()

                    if request.GET.get('Segnala Errori') == 'Segnala Errori':
                        rel = self.get_object().relatore
                        # doc = rel.split()
                        # doc_name = doc[0]
                        # doc_mail = doc[1]
                        doc_mail = rel.mail
                        doc_name = rel.nome + ' ' + rel.cognome
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

                        # return super().get(request, pk)
                        rt.delete()
                        return self.render_to_response(context_object_name)
    # controllare che chi si logga sia il relatore -- non funziona
    # def test_func(self):
    #     richiesta = self.get_object()
    #     nome = richiesta.relatore.split()
    #     if self.request.user.username == nome[0]:
    #         return True
    #     return False


# RICHIESTA PROVA FINALE


def provafin_richiesta(request):
    if request.method == "POST":
        form = RequestProvaFinaleForm(request.POST)
        if form.is_valid():
            r = request.user.username
            richiesta_create = form.save(commit=False)
            utente = User.objects.get(username=r)
            studente_log = Studente.objects.get(user=utente)
            richiesta_create.autore = studente_log
            if r != str(studente_log):
                messages.error(request, f'Autore deve essere lo studente {request.user.username}!')
                return redirect('provafin-richiesta')

            richiesta_create.save()
            messages.success(request, f'La richiesta di {request.user.username} è stata creata correttamente!')
            return redirect('profile')
    else:
        form = RequestProvaFinaleForm()
    return render(request, 'home/prova_finale_request.html', {'form': form})


def RichiestaAttInviate(request):
    all_studenti = Studente.objects.all()
    results = {}
    nome = request.user.username.split('.')
    for s in all_studenti:
        if s.nome == nome[0] and s.cognome == nome[1] and s.mail == request.user.email:
            results = Richiesta_prova_finale_inviata.objects.filter(autore=s).order_by('-date_posted')

    context = {
        #'all_richiesta_att': all_richiesta_att,
        'results': results,
        'title': "Le tue attività inviate: ",
        'no_results': "Non hai ancora inviato nessuna attività"
    }
    return render(request, 'home/index.html', context)





class RequestAttivitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Richiesta_prova_finale_bozza
    success_url = '/profile'


class RAPDetailView(DetailView):
    model = Richiesta_prova_finale_bozza
    template_name = 'home/detail_richiesta_attivita_template.html'

    def get(self, request, pk):
        rel = self.get_object().tutor
        # doc = rel.split()
        # doc_mail = doc[1]
        doc_mail = rel.mail
        author = self.get_object().autore
        stud_name = author.nome
        stud_surname = author.cognome

        rti = Richiesta_prova_finale_inviata()
        r = self.get_object()
        from_richiestaattivitabozza_to_richiestaattivitainviata(r, rti)
        # rti.autore = r.autore
        # rti.tutor = r.tutor
        # rti.argomento = r.argomento
        # rti.titolo_elaborato = r.titolo_elaborato
        # rti.tipologia = r.tipologia
        # rti.data_laurea = r.data_laurea
        # rti.save()

        if request.GET.get('Send') == 'Send':
            subject = 'Richiesta Prova Finale'
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
                'laurea': rti.data_laurea,
                'tipo': rti.tipologia,
                'titolo': rti.titolo_elaborato,
                'argomento': rti.argomento,
                'id': rti.id,
            }
            r.delete()
            html_template = get_template('home/richiesta_email_pfinale.html').render(context)
            message.attach_alternative(html_template, "text/html")
            message.send()

            messages.success(request, f'La mail è stata inviata correttamente al seguente indirizzo {doc_mail}!')
            return redirect('profile')

        else:
            rti.delete()
            return super().get(request, pk)


class AccettaRifiutaAttivitaDetailView(LoginRequiredMixin, DetailView):
    model = Richiesta_prova_finale_inviata
    template_name = "home/accept_provafinale.html"

    # success_url = '/'

    def get(self, request, pk):
        log = self.request.user.username
        log = log.split('.')
        self.object = self.get_object()
        tutor_n = self.object.tutor.nome
        tutor_c = self.object.tutor.cognome
        # rt = self.object.banama

        if log[0] != tutor_n or log[1] != tutor_c:
            # url = '/login/?next=/' + str(self.get_object().id) + '/accept_att'
            # messages.error(url, f'Errore! si puo loggare solo il docente tutor')
            # message = messages.error(request, f'Errore! si puo loggare solo il docente tutor')
            return redirect('/login/?next=/' + str(self.get_object().id) + '/accept_att')
        else:
            self.object = self.get_object()
            autore = self.object.autore
            context_object_name = {
                'name': self.object.autore,
                'argomento': self.object.argomento,
                'mail': self.object.autore.mail,
                'data': self.object.data_laurea,
                'tipo': self.object.tipologia,
                'titolo': self.object.titolo_elaborato,
            }
            if request.GET.get('Accetta') == 'Accetta':
                rel = self.get_object().tutor
                # doc = rel.split()
                # doc_name = doc[0]
                # doc_mail = doc[1]
                doc_name = rel.nome + ' ' + rel.cognome
                doc_mail = rel.mail
                author = self.get_object().autore
                stud_name = author.nome
                stud_surname = author.cognome
                subject = 'Accettata la Richiesta di Prova Finale'
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
                    'mail': doc_mail,
                }
                html_template = get_template('home/accetta_email.html').render(context)
                message.attach_alternative(html_template, "text/html")
                message.send()
                messages.success(request,
                                 f'La mail è stata inviata correttamente al seguente indirizzo {self.object.autore.mail}!')
                return redirect("/")
            else:
                if request.GET.get('Rifiuta') == 'Rifiuta':
                    rel = self.get_object().tutor
                    doc_name = rel.nome + ' ' + rel.cognome
                    doc_mail = rel.mail
                    author = self.get_object().autore
                    stud_name = author.nome
                    stud_surname = author.cognome
                    subject = 'Rifiutata la Richiesta di Prova Finale'
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
                    self.get_object().delete()
                    return redirect("/")
                else:
                    # se c'è errore allora
                    # rimette la tesi in richiesta tesi
                    rt = Richiesta_prova_finale_bozza()
                    r = self.get_object()
                    from_richiestaattivitainviata_to_richiestaattivitabozza(r, rt)
                    # rt.autore = r.autore
                    # rt.tutor = r.tutor
                    # rt.argomento = r.argomento
                    # rt.titolo_elaborato = r.titolo_elaborato
                    # rt.tipologia = r.tipologia
                    # rt.data_laurea = r.data_laurea

                    # rt.save()

                    if request.GET.get('Segnala Errori') == 'Segnala Errori':
                        rel = self.get_object().tutor
                        # doc = rel.split()
                        # doc_name = doc[0]
                        # doc_mail = doc[1]
                        doc_name = rel.nome + ' ' + rel.cognome
                        doc_mail = rel.mail
                        author = self.get_object().autore
                        stud_name = author.nome
                        stud_surname = author.cognome
                        subject = 'Errori nella Richiesta di Prova Finale'
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

                        # return super().get(request, pk)
                        rt.delete()
                        return self.render_to_response(context_object_name)


# controllare che chi si logga sia il relatore -- non funziona
def test_func(self):
    richiesta = self.get_object()
    nome = richiesta.relatore.split()
    if self.request.user.username == nome[0]:
        return True
    return False


# METODI PER EVITARE TANTI ASSEGNAMENTI


def from_richiestaattivitabozza_to_richiestaattivitainviata(rab, rai):
    rai.autore = rab.autore
    rai.tutor = rab.tutor
    rai.argomento = rab.argomento
    rai.titolo_elaborato = rab.titolo_elaborato
    rai.tipologia = rab.tipologia
    rai.data_laurea = rab.data_laurea
    rai.save()


def from_richiestaattivitainviata_to_richiestaattivitabozza(rai, rab):
    rab.autore = rai.autore
    rab.tutor = rai.tutor
    rab.argomento = rai.argomento
    rab.titolo_elaborato = rai.titolo_elaborato
    rab.tipologia = rai.tipologia
    rab.data_laurea = rai.data_laurea
    rab.modified = True
    rab.save()


def from_richiestatesiinviata_to_richiestatesibozza(ri, rb):
    rb.relatore = ri.relatore
    rb.correlatore = ri.correlatore
    rb.argomento = ri.argomento
    rb.tirocinio = ri.tirocinio
    rb.nome_azienda = ri.nome_azienda
    rb.data_laurea = ri.data_laurea
    rb.autore = ri.autore
    rb.modified = True
    rb.save()


def from_richiestatesibozza_to_richiestatesiinviata(rb, ri):
    ri.relatore = rb.relatore
    ri.correlatore = rb.correlatore
    ri.argomento = rb.argomento
    ri.tirocinio = rb.tirocinio
    ri.nome_azienda = rb.nome_azienda

    ri.autore = rb.autore
    ri.data_laurea = rb.data_laurea
    ri.save()


def from_tesicreata_to_richiestabozza(tc, rb):
    #rb.relatore = tc.relatore
    rb.correlatore = tc.correlatore
    rb.argomento = tc.argomento
    rb.tirocinio = tc.tirocinio
    rb.nome_azienda = tc.nome_azienda
    rb.data_inizio = tc.data_inizio
    rb.data_fine = tc.data_fine
    rb.date_posted = tc.date_posted
    rb.tag = tc.tag
    relatore = User.objects.get(username=tc.relatore)
    rb.relatore = Docente.objects.get(user=relatore)


def from_attprogettualecreata_to_richiestaProvabozza(ac, rb):
    rb.argomento = ac.argomento
    rb.date_posted = ac.date_posted
    tutor = User.objects.get(username=ac.tutor)
    rb.tutor = Docente.objects.get(user=tutor)


def from_attivitacreata_to_attivitaarchiviata(ac, aa):
    aa.author = ac.author
    aa.tutor = ac.tutor
    aa.argomento = ac.argomento
    aa.data_fine = ac.data_fine
    aa.data_inizio = ac.data_inizio
    aa.tag = ac.tag
    aa.save()
    ac.delete()


def from_tesicreata_to_tesiarchiviata(tc, ta):
    ta.author = tc.author
    ta.relatore = tc.relatore
    ta.argomento = tc.argomento
    ta.correlatore = tc.correlatore
    ta.data_fine = tc.data_fine
    ta.data_inizio = tc.data_inizio
    ta.tirocinio = tc.tirocinio
    ta.nome_azienda = tc.nome_azienda
    ta.tag = tc.tag
    ta.date_posted = tc.date_posted
    ta.save()
    tc.delete()
