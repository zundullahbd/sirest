from django.urls import path 
from .views import *

app_name = 'restopay'

urlpatterns = [
    path('', get_restopay, name='get_restopay'),
    path('tambah_saldo/', add_restopay, name='add_restopay'),
    path('tarik_saldo/', withdraw_restopay, name='withdraw_restopay'),
    path('jadwal/buat/', add_schedule, name="add_schedule"),
    path('jadwal/', get_all_schedule, name="get_all_schedule"),
    path('jadwal/ubah/<str:oldDay>', update_schedule, name="update_schedule"),
    path('jadwal/hapus/<str:hari>', delete_schedule, name="delete_schedule"),
    path('pesanan/', get_all_transaction, name="get_all_transaction"),
    path('pesanan/ongoing', get_ongoing_pesanan, name="get_ongoing_pesanan"),
    path('pesanan/detail', get_transaction_detail, name="get_transaction_detail"),
    path('pesanan/update', update_transaction, name="update_transaction"),
]

