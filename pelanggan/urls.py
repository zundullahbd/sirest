from django.urls import path
from . import views
from django.contrib import admin

app_name = 'pelanggan'

urlpatterns = [
    path('daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('daftar-menu/', views.dMenu, name='daftar-menu'),
    path('detail-menu/', views.detailMenu, name='detail-menu'),

]

