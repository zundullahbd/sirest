from django.urls import path
from . import views
from .views import *
from django.contrib import admin

app_name = 'kurir'

urlpatterns = [
    path('', views.kurirHome, name="kurir-home"),
]