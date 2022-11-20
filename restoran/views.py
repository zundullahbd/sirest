from django.shortcuts import render, redirect
from django.db import connection

def cm(request):
    return render(request, "formMakanan.html")

def dm(request):
    return render(request, "daftarMakanan.html")
    
def um(request):
    return render(request, "updateMakanan.html")
