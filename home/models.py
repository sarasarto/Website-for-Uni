from django.db import models
from users.models import Docente, Studente
from django.urls import reverse
from django.contrib.auth.models import User


class Tesi(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    relatore = models.ForeignKey(Docente, on_delete=models.CASCADE)
    correlatore = models.CharField(max_length=100)
    argomento = models.CharField(max_length=500)

    tirocinio_interno = models.BooleanField(default=False)
    tirocinio_azienda = models.BooleanField(default=False)
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
        return self.tutor + ' ' + self.argomento

    def get_absolute_url(self):
        return reverse('attivita-detail', kwargs={'pk': self.pk})


class Richiesta_tesi(models.Model):
    autore = models.ForeignKey(Studente, on_delete=models.CASCADE)
    relatore = models.CharField(max_length=100)
    correlatore = models.CharField(max_length=100)
    argomento = models.CharField(max_length=500)

    tirocinio_interno = models.BooleanField(default=False)
    tirocinio_azienda = models.BooleanField(default=False)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return self.autore.nome + ' ' + self.autore.cognome + ' ' + self.argomento


class Richiesta_prova_finale(models.Model):
    autore = models.ForeignKey(Studente, on_delete=models.CASCADE)
    tutor = models.CharField(max_length=100)
    argomento = models.CharField(max_length=500)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return self.autore.nome + ' ' + self.autore.cognome + ' ' + self.argomento
