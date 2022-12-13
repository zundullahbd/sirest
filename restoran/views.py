from django.db import connection
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;

def home(request):
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    name = request.session['rname'] + " " + request.session['rbranch']
    res = query(f"SELECT * FROM RESTAURANT WHERE RNAME = '{res_name}' AND rbranch='{r_branch}'")
    email1 = query(f"SELECT email FROM RESTAURANT WHERE RNAME = '{res_name}' AND rbranch='{r_branch}'")
    res1 = query(f"SELECT * FROM RESTAURANT_OPERATING_HOURS WHERE NAME = '{res_name}' AND branch='{r_branch}'")
    email2 = email1[0].get("email")
    print(email2)
    res2 = query(f"SELECT * FROM USER_ACC WHERE EMAIL = '{email2}'")
    nama_profil = res2[0].get("fname") + " " + res2[0].get("lname")
    res3 = query(f"SELECT * FROM TRANSACTION_ACTOR WHERE email = '{email2}'")

    context = {
        'name': res_name + " " + r_branch,
        'data_rest' : res,
        'data_operasi' :res1,
        'data_diri' : res2,
        'transaksi' : res3,
        'email2':email2,
        'namaprofil' : nama_profil,
        'phonenum': res2[0].get('phonenum'),
        'nik': res3[0].get('nik'),
        'bankname': res3[0].get('bankname'),
        'accountno': res3[0].get('accountno'),
        'rname' : res[0].get('rname'),
        'rbranch' : res[0].get('rbranch'),
        'rphonenum' : res[0].get('rphonenum'),
        'street' : res[0].get('street'),
        'district' : res[0].get('district'),
        'city' : res[0].get('city'),
        'province' : res[0].get('province'),
        'rating' : res[0].get('rating'),
        'rcategory' : res[0].get('rcategory'),
    }

    return render(request, 'restoran.html', context)

def get_all_makanan(request):
    context = {}
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    res = query(f"SELECT * FROM FOOD F INNER JOIN FOOD_CATEGORY FC ON FC.ID = F.FCATEGORY WHERE rname='{res_name}' AND rbranch='{r_branch}' ")
    ing =query(f"SELECT FI.FOODNAME, I.NAME FROM FOOD_INGREDIENTS FI, INGREDIENT I WHERE rname='{res_name}' AND rbranch='{r_branch}' AND FI.INGREDIENT = I.ID") 
    fc  = query(f"select name from food_category")
    ig = query(f"select name from ingredient")
    context = {
        "ingredients" : ing,
        "menu" : res,
        'name': res_name + " " + r_branch,
        'listKategori' : fc,
        'listBahan' : ig,
    }
    return render(request, "daftarMakanan.html", context)

def menu_makanan(request, valid=1):
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    print("gagal")
    fc  = query(f"select name from food_category")
    ig = query(f"select name from ingredient")
    context = {
        'listKategori' : fc,
        'listBahan' : ig,
        'name': res_name + " " + r_branch,
    }
    return render(request, 'formMakanan.html',context)

def add_makanan(request):
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    fi = query(f"select * from food_ingredients")

    context = {
        'name': res_name + " " + r_branch,
    }
    foodname = request.POST["foodname"]
    description = request.POST["description"]
    stock = request.POST["stock"]
    price = request.POST["price"]
    fcategory  = request.POST["fcategory"]
    ingredients = []
    for ingredient in request.POST.getlist('ingredient'):
        ingredients.append(ingredient)
    print(ingredients)

    if  foodname == '':
        return menu_makanan(request, 0)
    quer1 = query(f"SELECT id FROM FOOD_CATEGORY WHERE name = '{fcategory}'")
    hasil = quer1[0].get('id')
    hasil_ing = []
    for ing in ingredients:
        quer = query(f"SELECT id FROM INGREDIENT WHERE name = '{ing}'")
        id = quer[0].get('id')
        hasil_ing.append(id)

    quer3 = query(f"insert into food values('{res_name}','{r_branch}','{foodname}','{description}','{stock}','{price}','{hasil}')")
    for i in hasil_ing:
        quer = f"insert into food_ingredients values('{res_name}','{r_branch}','{foodname}','{i}')"
        temp = query(quer)
        print(temp)
    print(fi)
    return get_all_makanan(request)

@csrf_exempt  
def delete_makanan(request):
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    foodname= request.POST['foodname']
    print(foodname)
    ingredients = []
    for ingredient in request.POST.getlist('ingredient'):
        ingredients.append(ingredient)
        
    res = f"DELETE FROM FOOD_INGREDIENTS WHERE rname='{res_name}' AND rbranch = '{r_branch}' AND foodname = '{foodname}'"
    temp1 = query(res)
    #print(temp1)
    quer= f"DELETE FROM FOOD WHERE rname='{res_name}' AND rbranch = '{r_branch}' AND foodname = '{foodname}'"
    temp = query(quer)
    #print(temp)
    return get_all_makanan(request)

def update_makanan(request, foodname):
    print(foodname)
    res_name = request.session['rname']
    r_branch = request.session['rbranch']
    context = {}
    print(foodname)
    fc  = query(f"select name from food_category")
    ig = query(f"select name from food_ingredients FI left join ingredient I on FI.ingredient = I.id where rname='{res_name}' AND rbranch = '{r_branch}' AND foodname = '{foodname}'")
    bahan = query(f"select name from ingredient")
    
    print(ig)
    hasil_ig = []
    for i in range (len(ig)):
        hasil_ig.append(ig[i].get('name'))

    description = request.POST.get("description")
    stock = request.POST.get("stock")
    price = request.POST.get("price")
    fcategory  = request.POST.get("fcategory")
    
    ingredients = []
    for ingredient in request.POST.getlist('ingredient'):
        ingredients.append(ingredient)
    
    rm = []
    for ingredient in request.POST.getlist('ing'):
        rm.append(ingredient)
    print(rm)
    print(ingredients)
    context = {
        'listKategori' : fc,
        'bahan' : bahan,
        'foodname' : foodname,
        'name': res_name + " " + r_branch,
        'list' : hasil_ig
    }

    quer1 = query(f"SELECT id FROM FOOD_CATEGORY WHERE name = '{fcategory}'")
    
    print(fcategory)
    print(quer1)
    hasil =""
    for i in quer1:
        hasil = i['id']
    print(hasil)
    quer = query(f"UPDATE FOOD SET description = '{description}', stock = '{stock}', fcategory = '{hasil} WHERE  foodname = '{foodname}' AND rname='{res_name}' AND rbranch = '{r_branch}'")
     
    
    if len(ingredients) > 0:
        for i in ingredients:
            data = query(f"select id from ingredient where name = '{i}'")
            data = data[0].get("id")
            quer = query(f"INSERT INTO FOOD_INGREDIENTS VALUES ('{res_name}','{r_branch}','{foodname}','{data}')")
            print(quer)
    result = query(f"SELECT * FROM FOOD_INGREDIENTS WHERE rname='{res_name}' AND rbranch = '{r_branch}' AND foodname = '{foodname}'")
    print(result)
    return render(request, "updateMakanan.html",context)

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
        
def riwayat_pesanan_restoran(request):
    return render(request, 'riwayat_pesanan_restoran.html')