from django.urls import path
from . import views
from .views import *
from django.contrib import admin

app_name = 'kurir'

urlpatterns = [
    path('', views.kurirHome, name="kurir-home"),
    path('daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('daftar-restauran/<str:rname>/<str:rbranch>/detail/', views.detailRestauran, name='detail-restoran'),
    path('daftar-restauran/<str:rname>/<str:rbranch>/menu/', views.dMenu, name='dMenu'),
    path('kurir-riwayat_pesanan/', riwayat_pesanan_kurir, name='riwayat_pesanan_kurir'),
    path('list_pesanan_berlangsung/', list_pesanan_berlangsung, name='list_pesanan_berlangsung'),
    path('detail_pesanan_berlangsung/<str:id>/detail/', detail_pesanan_berlangsung, name='detail_pesanan_berlangsung'),
]