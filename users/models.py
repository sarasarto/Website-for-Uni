from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Docente(models.Model):
    nome = models.CharField(max_length=500)
    cognome = models.CharField(max_length=500)
    matricola = models.CharField(max_length=10)
    mail = models.CharField(max_length=1000)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome + '.' + self.cognome


class Studente(models.Model):
    nome = models.CharField(max_length=500)
    cognome = models.CharField(max_length=500)
    matricola = models.CharField(max_length=10)
    mail = models.CharField(max_length=1000)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome + '.' + self.cognome


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

