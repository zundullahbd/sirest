from django.urls import path
from . import views
from .views import *
from django.contrib import admin
from .views import *

app_name = 'pelanggan'

urlpatterns = [
    path('', views.pelangganHome, name="pelanggan-home"),
    path('daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('daftar-menu/', views.dMenu, name='daftar-menu'),
    # path('detail-menu/', views.detailMenu, name='detail-menu'),
    path('buat/', add_pesanan, name="add_pesanan"),
    path('ongoing/', get_ongoing_pesanan, name="get_ongoing_pesanan"),
    path('detail/', get_transaction_detail, name="get_transaction_detail"),
    path('list_cabang/', get_list_cabang, name="get_list_cabang"),
    path('list_makanan/', get_list_makanan, name="get_list_makanan"),
    path('daftar_pesanan/', get_daftar_pesanan, name="get_daftar_pesanan"),
    path('catatan/', add_catatan, name="add_catatan"),
    path('konfirmasi_pembayaran/', get_konfirmasi_pembayaran, name="get_konfirmasi_pembayaran"),
    path('ringkasan_pesanan/', get_ringkasan_pesanan, name="get_ringkasan_pesanan"),
    # path('pesanan/', get_all_schedule, name="get_all_schedule"),
    # path('', home, name="home"),
    path('daftar-restauran/<str:rname>/<str:rbranch>/detail/', detailRestauran, name='detail-restoran'),
    path('daftar-restauran/<str:rname>/<str:rbranch>/menu/', views.dMenu, name='dMenu'),
    path('histori-pesanan/pelanggan', get_transaction_history_pelanggan, name="get_transaction_history_pelanggan"),
    path('pelanggan-riwayat_pesanan/', riwayat_pesanan_pelanggan, name='riwayat_pesanan_pelanggan'),
    path('pelanggan-detail_riwayat_pesanan/', riwayat_pesanan_detail, name='riwayat_pesanan_detail'),
    path('pelanggan-penilaian_pesanan/', form_penilaian_pesanan, name='penilaian_pesanan'),

]

