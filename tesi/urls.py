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
from users import views as user_views
from home.views import TesiCreateView, PostDetailView, tesi_richiesta


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('profile/new', TesiCreateView.as_view(), name='tesi-create'),
    path('profile/richiesta', tesi_richiesta, name='tesi-richiesta'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('home.urls')),
]
