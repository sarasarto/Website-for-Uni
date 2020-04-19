from django.db import models
from users.models import Docente, Studente
from django.urls import reverse
from django.contrib.auth.models import User


class Tesi(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    relatore = models.ForeignKey(Docente, on_delete=models.CASCADE)
    correlatore = models.CharField(max_length=100)
    argomento = models.CharField(max_length=500)
    in_azienda = 'in azienda'
    interno = 'interno'
    scelte = [
        (in_azienda, 'in azienda'),
        (interno, 'interno'),
    ]
    tirocinio = models.CharField(max_length=500, choices=scelte, null=True)
    nome_azienda = models.CharField(max_length=1000, null=True, blank=True)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return str(self.argomento)

    def get_absolute_url(self):
        return reverse('tesi-detail', kwargs={'pk': self.pk})


class TesiArchiviata(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    relatore = models.ForeignKey(Docente, on_delete=models.CASCADE)
    correlatore = models.CharField(max_length=100)
    argomento = models.CharField(max_length=500)

    in_azienda = 'in azienda'
    interno = 'interno'
    scelte = [
        (in_azienda, 'in azienda'),
        (interno, 'interno'),
    ]
    tirocinio = models.CharField(max_length=500, choices=scelte, null=True)
    nome_azienda = models.CharField(max_length=1000, null=True, blank=True)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return str(self.argomento)

    def get_absolute_url(self):
        return reverse('tesi-detail', kwargs={'pk': self.pk})


class Attivita_progettuale(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tutor = models.ForeignKey(Docente, on_delete=models.CASCADE)
    argomento = models.CharField(max_length=500)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return str(self.argomento)

    def get_absolute_url(self):
        return reverse('attivita-detail', kwargs={'pk': self.pk})


class Attivita_progettuale_Archiviata(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tutor = models.ForeignKey(Docente, on_delete=models.CASCADE)
    argomento = models.CharField(max_length=500)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return str(self.argomento)

    def get_absolute_url(self):
        return reverse('attivita-detail', kwargs={'pk': self.pk})


class DateLauree(models.Model):
    data = models.DateTimeField()

    def __str__(self):
        return str(self.data)


class Richiesta_tesi(models.Model):
    autore = models.ForeignKey(Studente, on_delete=models.CASCADE, null=True)
    relatore = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    correlatore = models.CharField(max_length=100)
    argomento = models.CharField(max_length=500)

    in_azienda = 'in azienda'
    interno = 'interno'
    scelte = [
        (in_azienda, 'in azienda'),
        (interno, 'interno'),
    ]
    tirocinio = models.CharField(max_length=500, choices=scelte, null=True)
    nome_azienda = models.CharField(max_length=1000, null=True, blank=True)
    data_laurea = models.ForeignKey(DateLauree, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.autore.nome + ' ' + self.autore.cognome + ' ' + self.argomento

    def get_absolute_url(self):
        return reverse('richiesta-tesi-detail', kwargs={'pk': self.pk})

class Richiesta_tesi_inviata(models.Model):
    autore = models.ForeignKey(Studente, on_delete=models.CASCADE, null=True)
    relatore = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    correlatore = models.CharField(max_length=100)
    argomento = models.CharField(max_length=500)

    in_azienda = 'in azienda'
    interno = 'interno'
    scelte = [
        (in_azienda, 'in azienda'),
        (interno, 'interno'),
    ]
    tirocinio = models.CharField(max_length=500, choices=scelte, null=True)
    nome_azienda = models.CharField(max_length=1000, null=True, blank=True)
    data_laurea = models.ForeignKey(DateLauree, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.autore.nome + ' ' + self.autore.cognome + ' ' + self.argomento


class Richiesta_prova_finale(models.Model):
    tirocinio = 'tirocinio'
    attivita_progettuale = 'attivita_progettuale'
    altro = 'altro'
    scelte = [
        (tirocinio, 'tirocinio'),
        (attivita_progettuale, 'attivita_progettuale'),
        (altro, 'altro')
    ]
    autore = models.ForeignKey(Studente, on_delete=models.CASCADE, null=True)
    tutor = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    argomento = models.CharField(max_length=500)
    titolo_elaborato = models.CharField(max_length=500, null=True)
    tipologia = models.CharField(max_length=500, choices=scelte, null=True)
    data_laurea = models.ForeignKey(DateLauree, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.autore.nome + ' ' + self.autore.cognome + ' ' + self.argomento

    def get_absolute_url(self):
        return reverse('richiesta-prova-finale-detail', kwargs={'pk': self.pk})


class Richiesta_prova_finale_inviata(models.Model):
    tirocinio = 'tirocinio'
    attivita_progettuale = 'attivita_progettuale'
    altro = 'altro'
    scelte = [
        (tirocinio, 'tirocinio'),
        (attivita_progettuale, 'attivita_progettuale'),
        (altro, 'altro')
    ]
    autore = models.ForeignKey(Studente, on_delete=models.CASCADE, null=True)
    tutor = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    argomento = models.CharField(max_length=500)
    titolo_elaborato = models.CharField(max_length=500)
    tipologia = models.CharField(max_length=500, choices=scelte)
    data_laurea = models.ForeignKey(DateLauree, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.autore.nome + ' ' + self.autore.cognome + ' ' + self.argomento
