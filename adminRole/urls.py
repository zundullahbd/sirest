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




]

