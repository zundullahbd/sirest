from django.urls import path
from . import views
from .views import *
from django.contrib import admin

app_name = 'restoran'

urlpatterns = [
    path('', home, name="home"),
    path('create-makanan/', views.cm, name='makanan'),
    path('daftar-makanan/', views.dm, name='daftar-makanan'),
    path('update-makanan/', views.um, name='update-makanan'),
    path('jadwal/buat/', add_schedule, name="add_schedule"),
    path('jadwal/', get_all_schedule, name="get_all_schedule"),
    path('jadwal/ubah/<str:oldDay>', update_schedule, name="update_schedule"),
    path('jadwal/hapus/<str:hari>', delete_schedule, name="delete_schedule"),
    path('pesanan/', get_all_transaction, name="get_all_transaction"),
    path('pesanan/ongoing/', get_ongoing_pesanan, name="get_ongoing_pesanan"),
    path('pesanan/detail/', get_transaction_detail, name="get_transaction_detail"),
    path('pesanan/update/', update_transaction, name="update_transaction"),
<<<<<<< HEAD

    

=======
    path('restoran/promo', get_promo_restoran, name="get_promo_restoran"),
    path('restoran/promo-hari-spesial', restoran_detail_hariSpesial, name="restoran_detail_hariSpesial"),
    path('restoran/promo-min-transaction', restoran_detail_minTransaction, name="restoran_detail_minTransaction"),
>>>>>>> cf3b1d61f979b8cb1c1a949e9bfdd30669b6b6ee
    
]

