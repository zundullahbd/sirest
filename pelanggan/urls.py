from django.urls import path
from . import views
from .views import *
from django.contrib import admin
from .views import *

app_name = 'pelanggan'

urlpatterns = [
    path('', views.pelangganHome, name="pelanggan-home"),
    path('pelanggan/daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('pelanggan/daftar-menu/', views.dMenu, name='daftar-menu'),
    path('pelanggan/detail-menu/', views.detailMenu, name='detail-menu'),
    path('pelanggan/buat/', add_pesanan, name="add_pesanan"),
    path('pelanggan/ongoing/', get_ongoing_pesanan, name="get_ongoing_pesanan"),
    path('pelanggan/detail/', get_transaction_detail, name="get_transaction_detail"),
    path('pelanggan/list_cabang/', get_list_cabang, name="get_list_cabang"),
    path('pelanggan/list_makanan/', get_list_makanan, name="get_list_makanan"),
    path('pelanggan/daftar_pesanan/', get_daftar_pesanan, name="get_daftar_pesanan"),
    path('pelanggan/konfirmasi_pembayaran/', get_konfirmasi_pembayaran, name="get_konfirmasi_pembayaran"),
    path('pelanggan/ringkasan_pesanan/', get_ringkasan_pesanan, name="get_ringkasan_pesanan"),
    # path('pelanggan/pesanan/', get_all_schedule, name="get_all_schedule"),
    # path('pelanggan/', home, name="home"),
    path('pelanggan/detail-restoran/', views.detailRestauran, name='detail-restoran'),
    path('pelanggan/histori-pesanan/pelanggan', get_transaction_history_pelanggan, name="get_transaction_history_pelanggan"),

]

