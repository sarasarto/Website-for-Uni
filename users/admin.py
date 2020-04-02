from django.contrib import admin

from .models import Docente,Studente, Profile


admin.site.register(Docente)

admin.site.register(Studente)
admin.site.register(Profile)
