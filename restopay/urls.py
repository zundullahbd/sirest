from django.urls import path 
from .views import *

app_name = 'restopay'

urlpatterns = [
    path('', get_restopay, name='get_restopay'),
    path('tambah_saldo/', add_restopay, name='add_restopay'),
    path('tarik_saldo/', withdraw_restopay, name='withdraw_restopay'),
    
]

