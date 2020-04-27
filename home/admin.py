from django.contrib import admin
from .models import DateLauree, TesiCreata, Attivita_progettuale_creata, Richiesta_tesi_bozza, Richiesta_prova_finale_bozza,TesiArchiviata,\
     Attivita_progettuale_Archiviata, Richiesta_tesi_inviata , Richiesta_prova_finale_inviata , Prova

admin.site.register(DateLauree)
admin.site.register(TesiCreata)
admin.site.register(Attivita_progettuale_creata)
admin.site.register(Richiesta_tesi_bozza)
admin.site.register(Richiesta_prova_finale_bozza)
admin.site.register(TesiArchiviata)
admin.site.register(Attivita_progettuale_Archiviata)
admin.site.register(Richiesta_tesi_inviata)
admin.site.register(Richiesta_prova_finale_inviata)
admin.site.register(Prova)
