from django.db import connection
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;

def kurirHome(request):
    return render(request, "kurir.html")

def lihat_detail_pesanan(request):
    return render(request, "detail_pesanan_berlangsung.html")

def pesanan_terupdate(request):
    return render(request, "pesanan_terupdate.html")

def list_pesananan_berlangsung(request):
    return render(request, "list_pesanan_berlangsung.html")

