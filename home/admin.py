from django.contrib import admin
from .models import Tesi, Attivita_progettuale, Richiesta_tesi, Richiesta_prova_finale,TesiArchiviata,Attivita_progettuale_Archiviata

admin.site.register(Tesi)
admin.site.register(Attivita_progettuale)
admin.site.register(Richiesta_tesi)
admin.site.register(Richiesta_prova_finale)
admin.site.register(TesiArchiviata)
admin.site.register(Attivita_progettuale_Archiviata)