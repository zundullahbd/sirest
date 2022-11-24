from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from utils.query import query

def ctp(request):
    return render(request, "formTP.html")

def dtp(request):
    return render(request, "daftarTP.html")

def utp(request):
    return render(request, "updateTP.html")

def dashAdmin(request):
    return render(request, "home.html")

def cp(request):
    return render(request, "createPromo.html")

def fmt(request):
    return render(request, "form_min_transaksi.html")

def fhs(request):
    return render(request, "form_hari_spesial.html")

@csrf_exempt
def get_promo(request):
    
    res = query(f"SELECT P.PromoName, MTP.Id, SDP.Id FROM RESTAURANT_PROMO AS RP, PROMO AS P, MIN_TRANSACTION_PROMO AS MTP, SPECIAL_DAY_PROMO AS SDP WHERE RP.PId = P.Id AND RP.PId = MTP.Id AND RP.RName = 'Skynoodle' AND RP.RBranch = 'Glyburide';")
    
    for i in res:
        i['PId'] = str(i['PId'])

    context = {"total" : len(res), "list_promo": res}

    return render(request, "list_promo.html", context)

@csrf_exempt
def get_detail_hariSpesial(request):
    if request.method == "POST":
        RName = request.POST["RName"]
        RBranch = request.POST["RBranch"]
        PId = request.POST["PId"]

        restaurant_promo = query(f"SELECT RP.RName, Rp.RBranch FROM RESTAURANT_PROMO as RP, PROMO AS P WHERE RP.PId = P.Id")
        special_day_promo = query(f"SELECT SDP.Id, SDP.Date FROM SPECIAL_DAY_PROMO AS SDP, PROMO AS P WHERE SDP.Id = Promo.Id")
        promo = query(f"SELECT P.Id, P.PromoName, P.Discount FROM PROMO AS P, RESTAURANT_PROMO AS RP WHERE RP.PId = P.Id")
        
        context = {
            'restaurant_promo': restaurant_promo,
            'special_day_promo': special_day_promo,
            'promo': promo,
        }

        print(context)
        return render(request, "detail_promoHariSpesial.html", context)

@csrf_exempt
def get_detail_minTransaction(request):
    if request.method == "POST":
        RName = request.POST["RName"]
        RBranch = request.POST["RBranch"]
        PId = request.POST["PId"]

        restaurant_promo = query(f"SELECT RP.RName, Rp.RBranch FROM RESTAURANT_PROMO as RP, PROMO AS P WHERE RP.PId = P.Id")
        min_transaction_promo = query(f"SELECT MTP.Id, SDP.Date FROM MIN_TRANSACTION_PROMO AS MTP, PROMO AS P WHERE MTP.Id = Promo.Id")
        promo = query(f"SELECT P.Id, P.PromoName, P.Discount FROM PROMO AS P, RESTAURANT_PROMO AS RP WHERE RP.PId = P.Id")
        
        context = {
            'restaurant_promo': restaurant_promo,
            'min_transaction_promo': min_transaction_promo,
            'promo': promo,
        }

        print(context)
        return render(request, "detail_promoMinTransaction.html", context)