from django.urls import path 
from . import views
from .views import *

app_name = 'authentication'

urlpatterns = [
      path('register/', views.register_form, name='register'),
      path('login/', login, name='login'),
      path('logout/', logout, name='logout'),
      path('', views.homepage, name='homepage'),
      path('register/register-admin', views.register_admin, name='register-admin'),
      path('register/register-kurir', views.register_kurir, name='register-kurir'),
      path('register/register-pelanggan', views.register_pelanggan, name='register-pelanggan'),
      path('register/register-restoran', views.register_restoran, name='register-restoran'),



]
