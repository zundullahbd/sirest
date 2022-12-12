from django.db import connection
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;

def home(request):
    name = request.session['rname'] + " " + request.session['rbranch']
    return render(request, 'restoran.html', {'name': name})

def cm(request):
    return render(request, "formMakanan.html")

def dm(request):
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    res = query(f"SELECT * FROM FOOD F INNER JOIN FOOD_CATEGORY FC ON FC.ID = F.FCATEGORY WHERE rname='{res_name}' AND rbranch='{r_branch}' ")
    ing =query(f"SELECT FI.FOODNAME, I.NAME FROM FOOD_INGREDIENTS FI, INGREDIENT I WHERE rname='{res_name}' AND rbranch='{r_branch}' AND FI.INGREDIENT = I.ID") 
    print(ing)
    return render(request, "daftarMakanan.html", {"ingredients" : ing,"menu" : res,'name': res_name + " " + r_branch})

def um(request):
    return render(request, "updateMakanan.html")


def get_all_schedule(request):
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    res = query(f"SELECT * FROM RESTAURANT_OPERATING_HOURS WHERE name='{res_name}' AND Branch='{r_branch}' ")

    return render(request, "jadwal_resto.html", {"schedules" : res, "total": len(res), 'name': res_name + " " + r_branch})


def get_schedule_form(request):
    name = request.session['rname'] + " " + request.session['rbranch']
    return render(request, "create_jadwal.html", {'name' : name}) 

@csrf_exempt
def add_schedule(request):
    name = request.session['rname'] + " " + request.session['rbranch']
    if request.method != "POST":
        return get_schedule_form(request)
    
    context = {"isNotValid" : False, "message":"Harap masukan data yang lengkap", 'name' : name}

    hari = request.POST["hari"]
    jam_buka = request.POST["jam_buka"]
    jam_tutup = request.POST["jam_tutup"]

    context["isNotValid"] = not hari or  not jam_buka or not jam_tutup

    if(context["isNotValid"]):
        return render(request, "create_jadwal.html", context)
    
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    res = query(f"INSERT INTO RESTAURANT_OPERATING_HOURS VALUES ('{res_name}', '{r_branch}', '{hari}', '{jam_buka}', '{jam_tutup}')")

    return redirect("/restoran/jadwal")

@csrf_exempt
def update_schedule(request, oldDay):
    name = request.session['rname'] + " " + request.session['rbranch']
    res_name = request.session['rname']
    r_branch = request.session['rbranch']

    res = query(f"SELECT * FROM RESTAURANT_OPERATING_HOURS WHERE (Name, BRanch, day) = ('{res_name}', '{r_branch}', '{oldDay}')")[0]


    if request.method != "POST":
        oldValues = {
            "old_day" : oldDay,
            "old_open" : str(res["starthours"]),
            "old_close" : str(res["endhours"]),
            'name' : name
        }

        print(oldValues["old_open"])

        return render(request, "ubah_jadwal.html", oldValues)

    hari = request.POST.get("hari", res["day"])
    jam_buka = request.POST["jam_buka"]
    jam_tutup = request.POST["jam_tutup"]

    res = query(f"UPDATE RESTAURANT_OPERATING_HOURS SET starthours='{jam_buka}',endhours='{jam_tutup}' WHERE (Name, Branch, day) = ('{res_name}', '{r_branch}', '{hari}')")

    return redirect("/restoran/jadwal")

def delete_schedule(request, hari):
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    query(f"DELETE FROM RESTAURANT_OPERATING_HOURS WHERE (Name, Branch, day) = ('{res_name}', '{r_branch}', '{hari}')")

    return redirect("/restoran/jadwal")

@csrf_exempt
def get_all_transaction(request):
    name = request.session['rname'] + " " + request.session['rbranch']
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    
    res = query(f"SELECT * FROM USER_ACC JOIN (SELECT * FROM TRANSACTION_HISTORY TH JOIN TRANSACTION_STATUS TS ON TH.TSid=TS.id WHERE TH.Email IN (SELECT Email FROM TRANSACTION_FOOD WHERE (RName, Rbranch) = ('{res_name}', '{r_branch}'))) X USING(email)")
    
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_pesanan": res, 'name' : name}

    return render(request, "list_pesanan.html", context)

@csrf_exempt
def get_transaction_detail(request):
    name = request.session['rname'] + " " + request.session['rbranch']
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
            , 'name' : name
        }

        return render(request, "detail_pesanan.html", context)

def get_ongoing_pesanan(request):
    name = request.session['rname'] + " " + request.session['rbranch']
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    res = query(f"SELECT * FROM USER_ACC JOIN (SELECT * FROM TRANSACTION_HISTORY TH JOIN TRANSACTION_STATUS TS ON TH.TSid=TS.id WHERE TH.Email IN (SELECT Email FROM TRANSACTION_FOOD WHERE (RName, Rbranch) = ('{res_name}', '{r_branch}')) AND (TS.name ILIKE 'pending' OR TS.name ILIKE 'on%')) X USING(email)") 
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_pesanan": res, 'name' : name}

    return render(request, "ongoing_pesanan.html", context)

@csrf_exempt
def update_transaction(request):
    name = request.session['rname'] + " " + request.session['rbranch']
    if request.method == 'POST':
        email = request.POST["email"]
        time = request.POST["time"]
        status = request.POST["status"]

        if status == 'buat':
            id_status = query(f"SELECT id FROM TRANSACTION_STATUS WHERE name = 'on process'")[0]['id']
            print(id_status)

            query(f"UPDATE TRANSACTION_HISTORY SET TSid='{id_status}' WHERE (email, datetime) = ('{email}', '{time}')")

        if status == 'kirim':
            id_status = query(f"SELECT id FROM TRANSACTION_STATUS WHERE name = 'Complete'")[0]['id']

            courier_id = query(f"SELECT email from COURIER ORDER BY RANDOM() LIMIT 1")[0]['email']

            date = datetime.datetime.now()
            date= date.strftime("%Y-%m-%d %H:%M:%S")
            print(date, time)

            query(f"UPDATE TRANSACTION SET courierid='{courier_id}' WHERE (email, datetime) = ('{email}', '{time}') ")
            query(f"UPDATE TRANSACTION_HISTORY SET TSid='{id_status}', Datetimestatus='{date}' WHERE (email, datetime) = ('{email}', '{time}')")

    return redirect('/restoran/pesanan/ongoing')

@csrf_exempt
def get_promo_restoran(request):
    name = request.session['rname'] + " " + request.session['rbranch']
    res = query(f"SELECT P.PromoName, MTP.Id, SDP.Id FROM RESTAURANT_PROMO AS RP, PROMO AS P, MIN_TRANSACTION_PROMO AS MTP, SPECIAL_DAY_PROMO AS SDP WHERE RP.PId = P.Id AND RP.PId = MTP.Id AND RP.RName = 'Skynoodle' AND RP.RBranch = 'Glyburide';")
    
    for i in res:
        i['PId'] = str(i['PId'])

    context = {"total" : len(res), "list_promo_restoran": res, 'name' : name}

    return render(request, "list_promo_restoran.html", context)

@csrf_exempt
def restoran_detail_hariSpesial(request):
    name = request.session['rname'] + " " + request.session['rbranch']
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
            'promo': promo
            , 'name' : name
        }

        print(context)
        return render(request, "restoranDetailHariSpesial.html", context)

@csrf_exempt
def restoran_detail_minTransaction(request):
    name = request.session['rname'] + " " + request.session['rbranch']
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
            'name' : name
        }

        print(context)
        return render(request, "restoranDetailMinTransaction.html", context)
        
