from django.db import models
from users.models import Docente
from django.urls import reverse


class Tesi(models.Model):
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
        return reverse('post-detail', kwargs={'pk': self.pk})



class Attivita_progettuale(models.Model):
    tutor = models.ForeignKey(Docente, on_delete=models.CASCADE)
    argomento = models.CharField(max_length=500)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return self.tutor + ' ' + self.argomento

