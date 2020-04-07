from django.contrib import admin
from .models import DateLauree, Tesi, Attivita_progettuale, Richiesta_tesi, Richiesta_prova_finale,TesiArchiviata,\
    Attivita_progettuale_Archiviata, Richiesta_tesi_inviata , Richiesta_prova_finale_inviata

admin.site.register(DateLauree)
admin.site.register(Tesi)
admin.site.register(Attivita_progettuale)
admin.site.register(Richiesta_tesi)
admin.site.register(Richiesta_prova_finale)
admin.site.register(TesiArchiviata)
admin.site.register(Attivita_progettuale_Archiviata)
admin.site.register(Richiesta_tesi_inviata)
admin.site.register(Richiesta_prova_finale_inviata)