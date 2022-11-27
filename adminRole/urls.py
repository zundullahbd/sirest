from django.urls import path
from . import views
from django.contrib import admin
from .views import *

app_name = 'adminRole'

urlpatterns = [
    path('create-tarif-pengiriman/', views.ctp, name='tarif-pengiriman'),
    path('daftar-tarif-pengiriman/', views.dtp, name='daftar-tarif-pengiriman'),
    path('update-tarif-pengiriman/', views.utp, name='update-tarif-pengiriman'),
    path('', views.dashAdmin, name='dashboard-admin'),
    path('detail-aktorTransaksi/', views.detailAktor, name='detail-aktor'),
    path('create-promo/', views.cp, name='create-promo'),
    path('create-promo/min-transaksi.', views.fmt, name='create-promo-mintransaksi'),
    path('create-promo/hari-spesial.', views.fhs, name='create-promo-harispesial'),
    path('promo/', get_promo, name="get_promo"),
    path('promo/detail-hari-spesial', get_detail_hariSpesial, name="get_detail_hariSpesial"),
    path('promo/detail-min-transaction', get_detail_minTransaction, name="get_detail_minTransaction"),
    path('kategori_restoran/', get_all_kategori_restoran, name="get_all_kategori_restoran"),
    path('kategori_restoran/buat/', add_kategori_restoran, name="add_kategori_restoran"),
    path('kategori_restoran/ubah/', update_kategori_restoran, name="update_kategori_restoran"),
    path('kategori_restoran/hapus/', delete_kategori_restoran, name="delete_kategori_restoran"),
    path('bahan_makanan/', get_all_bahan_makanan, name="get_all_bahan_makanan"),
    path('bahan_makanan/buat/', add_bahan_makanan, name="add_bahan_makanan"),
    path('bahan_makanan/ubah/', update_bahan_makanan, name="update_bahan_makanan"),
    path('bahan_makanan/hapus/', delete_bahan_makanan, name="delete_bahan_makanan"),




]

