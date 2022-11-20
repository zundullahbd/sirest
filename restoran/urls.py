from django.urls import path
from . import views
from django.contrib import admin

app_name = 'restoran'

urlpatterns = [
    path('create-makanan/', views.cm, name='makanan'),
    path('daftar-makanan/', views.dm, name='daftar-makanan'),
    path('update-makanan/', views.um, name='update-makanan'),
]

