from django.db import connection
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;

def kurirHome(request):
    return render(request, "kurir.html")

def lihat_transaksi(request):
    return render(request, "lihat_transaksi.html")

def update_transaksi(request):
    return render(request, "update_transaksi.html")

