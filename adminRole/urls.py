from django.urls import path
from . import views
from django.contrib import admin

app_name = 'adminRole'

urlpatterns = [
    path('create-tarif-pengiriman/', views.ctp, name='tarif-pengiriman'),
    path('daftar-tarif-pengiriman/', views.dtp, name='daftar-tarif-pengiriman'),
    path('update-tarif-pengiriman/', views.utp, name='update-tarif-pengiriman'),
    path('', views.dashAdmin, name='dashboard-admin'),




]

