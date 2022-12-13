from django.urls import path
from . import views
from django.contrib import admin
from .views import *

app_name = 'adminRole'

urlpatterns = [
    path('daftar-tarif-pengiriman/create/', tarif_pengiriman, name='tarif-pengiriman'),
    path('daftar-tarif-pengiriman/create/post/', add_tarif, name='add-tarif-pengiriman'),
    path('daftar-tarif-pengiriman/', get_all_tarif, name='daftar-tarif-pengiriman'),
    path('daftar-tarif-pengiriman/delete/', delete_tarif, name="delete_fee"),
    path('daftar-tarif-pengiriman/<str:province>/', update_tarif, name="update-tarif-pengiriman"),
    path('', views.dashAdmin, name='dashboard-admin'),
    path('detail-aktorTransaksi/', views.detailAktor, name='detail-aktor'),
    path('create-promo/', views.cp, name='create-promo'),
    path('create-promo/min-transaksi.', views.fmt, name='create-promo-mintransaksi'),
    path('create-promo/hari-spesial.', views.fhs, name='create-promo-harispesial'),
    path('promo/', get_promo, name="get_promo"),
    path('promo/detail-hari-spesial', get_detail_hariSpesial, name="get_detail_hariSpesial"),
    path('promo/detail-min-transaction', get_detail_minTransaction, name="get_detail_minTransaction"),
    path('daftar-restauran/', views.dRestauran, name='daftar-restauran'),
    path('daftar-restauran/<str:rname>/<str:rbranch>/detail/', detailRestauran, name='detail-restoran'),
    path('daftar-restauran/<str:rname>/<str:rbranch>/menu/', views.dMenu, name='dMenu'),
    path('kategori_restoran/read/', get_all_kategori_restoran, name="get_all_kategori_restoran"),
    path('kategori_restoran/create/post/', add_kategori_restoran, name="add_kategori_restoran"),
    path('kategori_restoran/delete/', delete_kategori_restoran, name="delete_kategori_restoran"),
    path('kategori_restoran/create/', kategori_restoran, name="kategori_restoran"),
    path('bahan_makanan/read/', get_all_bahan_makanan, name="get_all_bahan_makanan"),
    path('bahan_makanan/create/post/', add_bahan_makanan, name="add_bahan_makanan"),
    path('bahan_makanan/delete/', delete_bahan_makanan, name="delete_bahan_makanan"),
    path('bahan_makanan/create/', bahan_makanan, name="bahan_makanan"),
    

    # path('kategori_makanan/', get_all_kategori_makanan, name="get_all_kategori_makanan"),
    # path('kategori_makanan/buat/', add_kategori_makanan, name="add_kategori_makanan"),
    # path('kategori_makanan/hapus/', delete_kategori_makanan, name="delete_kategori_makanan"),

    path('kategori_makanan/create/', kategori_makanan, name='kategori_makanan'),
    path('kategori_makanan/read/', get_all_kategori_makanan, name='get_all_kategori_makanan'),
    path('kategori_makanan/delete/', delete_kategori_makanan, name='delete_kategori_makanan'),
    path('kategori_makanan/create/post/', add_kategori_makanan, name='add_kategori_makanan'),
    # path('kategori_makanan/create/post/', posts, name='post'),



]

