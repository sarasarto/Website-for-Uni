from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'home'

urlpatterns = [
    # /home/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /home/login
    url(r'login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'logout/$', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
