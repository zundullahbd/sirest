from django.urls import path
from . import views
from django.contrib import admin
from .views import *

app_name = 'pelanggan'

urlpatterns = [
    path('', views.pelangganHome, name="pelanggan-home"),
    path('daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('daftar-menu/', views.dMenu, name='daftar-menu'),
    path('detail-restoran/', views.detailRestauran, name='detail-restoran'),
    path('histori-pesanan/pelanggan', get_transaction_history_pelanggan, name="get_transaction_history_pelanggan"),

]

