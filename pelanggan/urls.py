from django.urls import path
from . import views
from django.contrib import admin
from .views import *

app_name = 'pelanggan'

urlpatterns = [
    path('daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('daftar-menu/', views.dMenu, name='daftar-menu'),
    path('detail-menu/', views.detailMenu, name='detail-menu'),
    path('histori-pesanan/pelanggan', get_transaction_history_pelanggan, name="get_transaction_history_pelanggan"),

]

