from django.db import models
from users.models import Docente

class Tesi(models.Model):
    relatore = models.ForeignKey(Docente, on_delete=models.CASCADE)
    correlatore = models.CharField(max_length=100)
    argomento = models.CharField(max_length=500)
    # 1 interno , 0 in azienda
    tirocinio = models.BooleanField(default=False)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return self.relatore + ' ' + self.argomento + ' ' + self.tirocinio


class Attivita_progettuale(models.Model):
    tutor = models.ForeignKey(Docente, on_delete=models.CASCADE)
    argomento = models.CharField(max_length=500)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    tag = models.IntegerField()

    def __str__(self):
        return self.tutor + ' ' + self.argomento

