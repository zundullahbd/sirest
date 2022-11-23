from django.shortcuts import render, redirect
from django.db import connection

def ctp(request):
    return render(request, "formTP.html")

def dtp(request):
    return render(request, "daftarTP.html")

def utp(request):
    return render(request, "updateTP.html")

def dashAdmin(request):
    return render(request, "home.html")
