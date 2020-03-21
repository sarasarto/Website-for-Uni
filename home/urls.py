from django.urls import path, include
from . import views

from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'home'

urlpatterns = [
    # /home/
    url(r'^$', views.IndexView.as_view(), name='index'),

]
