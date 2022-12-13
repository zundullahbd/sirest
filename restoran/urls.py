from django.urls import path
from . import views
from .views import *
from django.contrib import admin

app_name = 'restoran'

urlpatterns = [
    path('', home, name="home"),
    path('jadwal/buat/', add_schedule, name="add_schedule"),
    path('jadwal/', get_all_schedule, name="get_all_schedule"),
    path('jadwal/ubah/<str:oldDay>', update_schedule, name="update_schedule"),
    path('jadwal/hapus/<str:hari>', delete_schedule, name="delete_schedule"),
    path('pesanan/', get_all_transaction, name="get_all_transaction"),
    path('pesanan/ongoing/', get_ongoing_pesanan, name="get_ongoing_pesanan"),
    path('pesanan/detail/', get_transaction_detail, name="get_transaction_detail"),
    path('pesanan/update/', update_transaction, name="update_transaction"),
    path('menu/create/', menu_makanan, name='create-menu-makanan'),
    path('menu/create/post/', add_makanan, name='add-makanan'),
    path('menu/', get_all_makanan, name='daftar-menu-makanan'),
    path('menu/delete/', delete_makanan, name="delete_makanan"),
    path('menu/<str:foodname>/', update_makanan, name="update-makanan"),
    path('restoran-riwayat_pesanan/', riwayat_pesanan_restoran, name='riwayat_pesanan_restoran') 
     
]

