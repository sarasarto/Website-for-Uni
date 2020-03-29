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
from home import views
from users import views as user_views
from home.views import (
    TesiCreateView,
    AttivitaCreateView,
    TesiDetailView,
    AttivitaDetailView,
    TesiUpdateView,
    AttivitaUpdateView,
    TesiDeleteView,
    AttivitaDeleteView,
    tesi_richiesta,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('tesi/', views.show_tesi, name='tesi'),
    path('attivita/', views.show_attivita, name='attivita'),

    # per la tesi
    path('profile/new_tesi', TesiCreateView.as_view(), name='tesi-create'),
    path('<int:pk>/detail_tesi', TesiDetailView.as_view(), name='tesi-detail'),
    path('<int:pk>/update_tesi', TesiUpdateView.as_view(), name='tesi-update'),
    path('<int:pk>/delete_tesi', TesiDeleteView.as_view(), name='tesi-delete'),


    # per l'attivita
    path('profile/new_attivita', AttivitaCreateView.as_view(), name='attivita-create'),
    path('<int:pk>/detail_att', AttivitaDetailView.as_view(), name='attivita-detail'),
    path('<int:pk>/update_att', AttivitaUpdateView.as_view(), name='attivita-update'),
    path('<int:pk>/delete_att', AttivitaDeleteView.as_view(), name='attivita-delete'),


    path('profile/richiesta', tesi_richiesta, name='tesi-richiesta'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('home.urls')),
]
