from django.shortcuts import render, redirect
from django.db import connection

def dMenu(request):
    return render(request, "daftarMenu.html")

def dRestauran(request):
    return render(request, "daftarRestauran.html")

def detailMenu(request):
    return render(request, "detailMenu.html")