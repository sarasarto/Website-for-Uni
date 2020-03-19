from django.db import models
from django.urls import reverse

class Docente(models.Model):
    nome = models.CharField(max_length=500)
    cognome = models.CharField(max_length=500)
    mail = models.CharField(max_length=1000)

    def __str__(self):
        return self.nome + ' ' + self.cognome


class Studente(models.Model):
    nome = models.CharField(max_length=500)
    cognome = models.CharField(max_length=500)
    matricola = models.CharField(max_length=10)
    mail = models.CharField(max_length=1000)

    def __str__(self):
        return self.cognome + ' ' + self.matricola


class Progetto(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    titolo = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=1000)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return self.titolo
