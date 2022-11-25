from django.urls import path
from . import views
from .views import *
from django.contrib import admin

app_name = 'pelanggan'

urlpatterns = [
    path('daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('daftar-menu/', views.dMenu, name='daftar-menu'),
    path('detail-menu/', views.detailMenu, name='detail-menu'),
    path('buat/', add_pesanan, name="add_pesanan"),
    path('ongoing/', get_ongoing_pesanan, name="get_ongoing_pesanan"),
    path('detail/', get_transaction_detail, name="get_transaction_detail"),
    path('list_cabang/', get_list_cabang, name="get_list_cabang"),
    path('list_makanan/', get_list_makanan, name="get_list_makanan"),
    path('daftar_pesanan/', get_daftar_pesanan, name="get_daftar_pesanan"),
    path('konfirmasi_pembayaran/', get_konfirmasi_pembayaran, name="get_konfirmasi_pembayaran"),
    path('ringkasan_pesanan/', get_ringkasan_pesanan, name="get_ringkasan_pesanan"),
    # path('pesanan/', get_all_schedule, name="get_all_schedule"),
    path('', home, name="home"),
]

