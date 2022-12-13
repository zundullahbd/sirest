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

def dMenu(request, rname, rbranch):
    res = query(f"SELECT * FROM FOOD WHERE rname='{rname}' AND rbranch='{rbranch}' ")
    res = query(f"SELECT * FROM FOOD WHERE rname='{rname}' AND rbranch='{rbranch}' ")

    fc  = query(f"select * from food_category")
    ig = query(f"select FOODNAME, INGREDIENT, NAME  from FOOD_INGREDIENTS FI LEFT JOIN INGREDIENT I ON FI.INGREDIENT = I.ID WHERE rname='{rname}' AND rbranch='{rbranch}'")
    context = {
        "menu" : res,
        'listKategori' : fc,
        'listBahan' : ig,
    }
    return render(request, "daftarMenu.html",context)

def dRestauran(request):
    context = {}
    res = query(f"select * from restaurant")
    context = {
        'listRestauran' : res,
    }
    return render(request, "daftarRestauran.html", context)

def detailRestauran(request,rname, rbranch):
    context = {}
    res = query(f"select * from restaurant where rname = '{rname}' AND rbranch = '{rbranch}'")
    res1 = query(f"select * from restaurant_operating_hours where name = '{rname}' AND branch = '{rbranch}'")
    res2 = query(f"select P.promoName from restaurant_promo RO, promo P where RO.rname = '{rname}' AND RO.rbranch = '{rbranch}' AND RO.PId = P.ID")
    res3 = query(f"select * from restaurant_category")

    print(res[0].get('rname'))
    print(res1)
    print(res2)
    context = {
        'rname' : res[0].get('rname'),
        'rbranch' : res[0].get('rbranch'),
        'rphonenum' : res[0].get('rphonenum'),
        'street' : res[0].get('street'),
        'district' : res[0].get('district'),
        'city' : res[0].get('district'),
        'province' : res[0].get('province'),
        'rating' : res[0].get('rating'),
        'rating' : res[0].get('rating'),
        'rcategory' : res[0].get('rcategory'),
        'op' : res1,
        'promo' :res2,
        'cat' : res3,
    }
    return render(request, "detailRestauran.html",context)