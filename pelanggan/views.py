from django.shortcuts import render, redirect
from django.db import connection
from utils.query import query

from django.db import connection
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;

def pelangganHome(request):
    return render(request, 'pelanggan.html')
def dMenu(request):
    return render(request, "daftarMenu.html")

def dRestauran(request):
    return render(request, "daftarRestauran.html")

def detailMenu(request):
    return render(request, "detailMenu.html")

def home(request):
    return render(request, 'pelanggan.html')

def get_pesanan_form(request):
    return render(request, "create_pesanan.html") 

@csrf_exempt
def add_pesanan(request):
    
    if request.method != "POST":
        return get_pesanan_form(request)
    
    context = {"isNotValid" : False, "message":"Harap masukan data yang lengkap"}

    jalan = request.POST["jalan"]
    kecamatan = request.POST["kecamatan"]
    kota = request.POST["kota"]
    provinsi = request.POST["provinsi"]

    context["isNotValid"] = not jalan or not kecamatan or not kota or not provinsi

    if(context["isNotValid"]):
        return render(request, "create_pesanan.html", context)
    
    # res_name = request.session['rname']
    # r_branch = request.session['rbranch']
    # res = query(f"INSERT INTO RESTAURANT_OPERATING_HOURS VALUES ('{res_name}', '{r_branch}', '{jalan}', '{kecamatan}', '{kota}')")

    return redirect("/pelanggan/list_cabang")

def get_ongoing_pesanan(request):
    # res_name = request.session['rname']
    # r_branch = request.session['rbranch']
    res_name = 'Yacero'
    r_branch = 'THE'
    res = query(f"SELECT * FROM USER_ACC JOIN (SELECT * FROM TRANSACTION_HISTORY TH JOIN TRANSACTION_STATUS TS ON TH.TSid=TS.id WHERE TH.Email IN (SELECT Email FROM TRANSACTION_FOOD WHERE (RName, Rbranch) = ('{res_name}', '{r_branch}')) AND (TS.name ILIKE 'pending' OR TS.name ILIKE 'on%')) X USING(email)") 
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_pesanan": res, 'rname':res_name, 'rbranch':r_branch}

    return render(request, "ongoing_pelanggan.html", context)

@csrf_exempt
def get_transaction_detail(request):
    if request.method == "POST":
        email = request.POST["email"]
        time = request.POST["time"]

        transaction_status = query(f"SELECT NAME from TRANSACTION_STATUS WHERE Id IN ( SELECT TSID FROM TRANSACTION_HISTORY WHERE (Email, datetime) = ('{email}', '{time}'))")[0]['name']
        transaction = query(f"SELECT * FROM TRANSACTION WHERE (Email, datetime) = ('{email}', '{time}')")[0]
        payment_method = query(f"SELECT * FROM PAYMENT_METHOD WHERE id='{transaction['pmid']}'") 
        payment_status = query(f"SELECT * FROM PAYMENT_status WHERE id='{transaction['psid']}'") 
        foods = query(f"SELECT * FROM TRANSACTION_FOOD WHERE (Email, Datetime) = ('{email}', '{time}')")
        courier = query(f"select * FROM COURIER WHERE EMail= '{transaction['courierid']}'")[0]
        courier_name = query(f"SELECT * FROM USER_ACC WHERE EMAIL='{courier['email']}'")[0]
        courier_name = courier_name['fname'] + " " + courier_name['lname']
        restaurant = query(f"SELECT * FROM RESTAURANT WHERE (Rname, Rbranch) = ('{foods[0]['rname']}', '{foods[0]['rbranch']}')")
        customer = query(f"SELECT * FROM USER_ACC WHERE EMAIL = '{email}'")[0]
        
        food_price=0
        for i in foods:
            j = query(f"SELECT PRICE FROM FOOD WHERE (Rname, Rbranch, foodname) = ('{i['rname']}','{i['rbranch']}','{i['foodname']}')")
            food_price+= j[0]['price']
        
        
        context = {
            'transaction': transaction,
            'transaction_status': transaction_status,
            'payment_method': payment_method[0]['name'],
            'payment_status': payment_status[0]['name'],
            'foods' : foods,
            'courier': courier,
            'courier_name': courier_name,
            'restaurant': restaurant[0],
            'customer' : customer,
            'total_food_price': food_price
        }

        print(context)
        return render(request, "detail_pesanan.html", context)


def get_list_cabang(request):
    # provinsi = request.session['provinsi']
    # res = query(f"""select row_number() over() as "row", r.rname || ' ' || r.rbranch restoran, p.promoname promo 
    #                     from restaurant r 
    #                     join restaurant_promo rp 
    #                         on r.rname = rp.rname and r.rbranch = rp.rbranch 
    #                     join promo p 
    #                         on p.id = rp.pid 
    #                     WHERE r.province = '{provinsi}'""") 

    # context = {"list_cabang": res}

    return render(request, "pilih_cabang.html")

@csrf_exempt
def get_list_makanan(request):
    # provinsi = request.session['provinsi']
    # res = query(f"""select row_number() over() as "row", r.rname || ' ' || r.rbranch restoran, p.promoname promo 
    #                     from restaurant r 
    #                     join restaurant_promo rp 
    #                         on r.rname = rp.rname and r.rbranch = rp.rbranch 
    #                     join promo p 
    #                         on p.id = rp.pid 
    #                     WHERE r.province = '{provinsi}'""") 

    # context = {"list_makanan": res}

    return render(request, "pilih_makanan.html")

@csrf_exempt
def get_daftar_pesanan(request):
    # provinsi = request.session['provinsi']
    # res = query(f"""select row_number() over() as "row", r.rname || ' ' || r.rbranch restoran, p.promoname promo 
    #                     from restaurant r 
    #                     join restaurant_promo rp 
    #                         on r.rname = rp.rname and r.rbranch = rp.rbranch 
    #                     join promo p 
    #                         on p.id = rp.pid 
    #                     WHERE r.province = '{provinsi}'""") 

    # context = {"daftar_pesanan": res}

    return render(request, "daftar_pesanan.html")

@csrf_exempt
def get_konfirmasi_pembayaran(request):
    # provinsi = request.session['provinsi']
    # res = query(f"""select row_number() over() as "row", r.rname || ' ' || r.rbranch restoran, p.promoname promo 
    #                     from restaurant r 
    #                     join restaurant_promo rp 
    #                         on r.rname = rp.rname and r.rbranch = rp.rbranch 
    #                     join promo p 
    #                         on p.id = rp.pid 
    #                     WHERE r.province = '{provinsi}'""") 

    # context = {"konfirmasi_pembayaran": res}

    return render(request, "konfirmasi_pembayaran.html")

@csrf_exempt
def get_ringkasan_pesanan(request):
    # provinsi = request.session['provinsi']
    # res = query(f"""select row_number() over() as "row", r.rname || ' ' || r.rbranch restoran, p.promoname promo 
    #                     from restaurant r 
    #                     join restaurant_promo rp 
    #                         on r.rname = rp.rname and r.rbranch = rp.rbranch 
    #                     join promo p 
    #                         on p.id = rp.pid 
    #                     WHERE r.province = '{provinsi}'""") 

    # context = {"ringkasan_pesanan": res}

    return render(request, "ringkasan_pesanan.html")
def detailRestauran(request):
    return render(request, "detailRestauran.html")

def get_transaction_history_pelanggan(request):
    
    res = query(f"SELECT R.RName, U.FName, U.LName, TH.DatetimeStatus, TS.Name, R.Rating FROM FROM RESTAURANT AS R, USER_ACC AS U, TRANSACTION_HISTORY AS TH, TRANSACTION_STATUS AS TS, COURIER AS C, TRANSACTION_ACTOR AS TA, FOOD AS F, TRANSACTION_FOOD AS TF, TRANSACTION AS T, CUSTOMER AS C WHERE TA.Email = U.Email AND C.Email = TA.Email AND R.Email = TA.Email AND F.RName = R.RName AND F.RBranch = R.RBranch AND TF.RName = F.RName AND TF.RBranch = F.RBranch AND TH.Email = T.Email AND TH.Datetime = TF.Datetime AND TH.TSId = TS.Id AND U.FName = 'Ara' AND U.LName = 'Rapkins'") 
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_transaction_history_pelanggan": res}

    return render(request, "listTransactionHistoryPelanggan.html", context)
