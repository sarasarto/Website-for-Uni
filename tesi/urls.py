"""tesi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

import attivita
from attivita import views
from attivita.views import (
    AttivitaDetailView,
    AttivitaCreate,
    AttivitaUpdateView,
    AttivitaDeleteView,
    AttivitaArchiviataDetailView,
    RequestAttivitaDetailView,
    RequestAttivitaUpdateView,
)
from home import views
from users import views as user_views
from home.views import (
    #TesiCreateView,
    #AttivitaCreateView,
    TesiDetailView,

    TesiUpdateView,

    TesiDeleteView,

    tesi_richiesta,
    provafin_richiesta,
    RequestTesiDetailView,

    RTDetailView,
    RAPDetailView,
    AccettaRifiutaTesiDetailView,
    AccettaRifiutaAttivitaDetailView,
    RichiestaTesiInviate,
    RichiestaAttInviate,
    RequestTesiUpdateView,

    RequestTesiDeleteView,
    RequestAttivitaDeleteView,IndexView,TesiDetailView,TesiArchiviataDetailView

)

urlpatterns = [

    path('prova/', views.prova, name='prova'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('cerca/', views.cerca, name='cerca'),


    path('profile/', user_views.profile, name='profile'),
    path('tesi/', views.show_tesi, name='tesi'),
    path('attivita/', attivita.views.show_attivita, name='attivita'),
    path('tesi_archiviata/', views.show_tesi_archiviate, name='t_archiviata'),

    path('tesi_accettate/', views.show_tesi_accettate, name='t-accettate'),
    path('att_accettate/', attivita.views.show_attivita_accettate, name='att-accettate'),
    path('tesi_archiviata/<int:pk>/detail', TesiArchiviataDetailView.as_view(), name='t_archiviata_detail'),


    path('att_archiviata/', attivita.views.show_att_archiviate, name='att_archiviata'),
    path('att_archiviata/<int:pk>/detail', AttivitaArchiviataDetailView.as_view(), name='att_archiviata_detail'),

    # per la tesi
    #path('profile/new_tesi', TesiCreateView.as_view(), name='tesi-create'),
    path('profile/new_tesi', views.TesiCreate, name='tesi-create'),
    path('<int:pk>/detail_tesi', TesiDetailView.as_view(), name='tesi-detail'),
    path('<int:pk>/update_tesi', TesiUpdateView.as_view(), name='tesi-update'),
    path('<int:pk>/delete_tesi', TesiDeleteView.as_view(), name='tesi-delete'),

    path('<int:pk>/accept_tesi', AccettaRifiutaTesiDetailView.as_view(), name='accept-request-tesi'),
    path('<int:pk>/accept_att', AccettaRifiutaAttivitaDetailView.as_view(), name='accept-request-att'),

    # per l'attivita
    #path('profile/new_attivita', AttivitaCreateView.as_view(), name='attivita-create'),
    path('profile/new_attivita', AttivitaCreate, name='attivita-create'),
    path('<int:pk>/detail_att', AttivitaDetailView.as_view(), name='attivita-detail'),
    path('<int:pk>/update_att', AttivitaUpdateView.as_view(), name='attivita-update'),
    path('<int:pk>/delete_att', AttivitaDeleteView.as_view(), name='attivita-delete'),


    #richiesta tesi e prova finale
    path('profile/richiesta_tesi', tesi_richiesta, name='tesi-richiesta'),
    path('<int:pk>/detail_richiesta_tesi/', RTDetailView.as_view(), name='richiesta-tesi-detail'),
    path('<int:pk>/update_tesi_request/', RequestTesiUpdateView.as_view(), name='richiesta-tesi-update'),
    path('<int:pk>/delete_tesi_request/', RequestTesiDeleteView.as_view(), name='richiesta-tesi-delete'),


    path('<int:pk>/detail_tesi/tesi_request/', RequestTesiDetailView.as_view(), name='tesi-request-precompiled'),
    path('profile/richieste_tesi_inviate/', RichiestaTesiInviate, name='tesi-inviate'),

    path('profile/richiesta_prova', provafin_richiesta, name='provafin-richiesta'),
    path('<int:pk>/detail_richiesta_prova_finale', RAPDetailView.as_view(), name='richiesta-prova-finale-detail'),
    path('<int:pk>/update_attivita_request/', RequestAttivitaUpdateView.as_view(), name='richiesta-attivita-update'),
    path('<int:pk>/delete_attivita_request/', RequestAttivitaDeleteView.as_view(), name='richiesta-attivita-delete'),
    path('<int:pk>/detail_att/attivita_request/', RequestAttivitaDetailView.as_view(), name='attivita-request-precompiled'),
    path('profile/richieste_att_inviate/', RichiestaAttInviate, name='att-inviate'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', IndexView.as_view(), name='index'),

]
