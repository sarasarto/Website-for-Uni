from django.contrib import admin

from .models import Docente,Progetto,Studente


admin.site.register(Docente)
admin.site.register(Progetto)
admin.site.register(Studente)