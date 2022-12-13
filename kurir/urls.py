from django.urls import path
from . import views
from .views import *
from django.contrib import admin

app_name = 'kurir'

urlpatterns = [
    path('', views.kurirHome, name="kurir-home"),
    path('detail_pesanan_berlangsung/', views.lihat_detail_pesanan, name="detail-pesanan"),
    path('pesanan_terupdate/', views.pesanan_terupdate, name="pesanan-terupdate"),
    path('list_pesanan_berlangsung/', views.list_pesananan_berlangsung, name="list-pesanan-berlangsung"),
    path('daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('daftar-restauran/<str:rname>/<str:rbranch>/detail/', detailRestauran, name='detail-restoran'),
    path('daftar-restauran/<str:rname>/<str:rbranch>/menu/', views.dMenu, name='dMenu'),
]