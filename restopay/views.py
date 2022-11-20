from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;
# Create your views here.


def get_restopay(request):
    res = query("SELECT RESTOPAY, bankname, accountno FROM TRANSACTION_ACTOR WHERE Email='spritchett5@earthlink.net'")[0]
    restopay = '{:,}'.format( res['restopay'])
    bank = res['bankname']
    account = res['accountno']
    return render(request,"restopay.html", {"balance": restopay, "bank" : bank, 'account': account})

def get_form_restopay(request, type):

    res = query("SELECT RESTOPAY, bankname, accountno FROM TRANSACTION_ACTOR WHERE Email='spritchett5@earthlink.net'")[0]
    restopay = '{:,}'.format( res['restopay'])
    bank = res['bankname']
    account = res['accountno']

    if (type == "tambah_saldo"):
        return render(request, "tambah_restopay.html", {"balance": restopay, "bank" : bank, 'account': account})
    
    return render(request, "tarik_restopay.html", {"balance": restopay, "bank" : bank, 'account': account})

@csrf_exempt
def add_restopay(request):
    context = {"isNotValid" : False, "message":"input tidak valid"}

    if request.method != "POST":
        return get_form_restopay(request, "tambah_saldo")
    
    nominal = str(request.POST["nominal"])

    context["isNotValid"] = not nominal or  not nominal.isdigit(); 
    
    res = query("SELECT RESTOPAY, bankname, accountno FROM TRANSACTION_ACTOR WHERE Email='spritchett5@earthlink.net'")[0]
    context['restopay'] = '{:,}'.format( res['restopay'])
    context['bank']  = res['bankname']
    context['account'] = res['accountno']

    if(context["isNotValid"]):
        return render(request, "tambah_restopay.html", context)
    
    response = query(f"UPDATE TRANSACTION_ACTOR SET RESTOPAY='{nominal}' WHERE EMAIL='spritchett5@earthlink.net'");
    if(response == "Jumlah saldo tidak mencukupi."):
        context["isNotValid"] = True
        context["message"] = response
        return render(request, "tambah_restopay.html", context)

    return redirect("/restopay")


@csrf_exempt
def withdraw_restopay(request):
    context = {"isNotValid" : False, "message":"input tidak valid"}

    if request.method != "POST":
        return get_form_restopay(request, "tarik_saldo")
    
    nominal = str(request.POST["nominal"])

    context["isNotValid"] = not nominal or  not nominal.isdigit(); 
    
    res = query("SELECT RESTOPAY, bankname, accountno FROM TRANSACTION_ACTOR WHERE Email='spritchett5@earthlink.net'")[0]
    context['restopay'] = '{:,}'.format( res['restopay'])
    context['bank']  = res['bankname']
    context['account'] = res['accountno']

    if(context["isNotValid"]):
        return render(request, "tarik_restopay.html", context)
    
    nominal = int(nominal)
    response = query(f"UPDATE TRANSACTION_ACTOR SET RESTOPAY='{nominal*-1}' WHERE EMAIL='spritchett5@earthlink.net'");
    if(response == "Jumlah saldo tidak mencukupi."):
        context["isNotValid"] = True
        context["message"] = response
        return render(request, "tarik_restopay.html", context)

    return redirect("/restopay")


def get_all_schedule(request):
    res = query("SELECT * FROM RESTAURANT_OPERATING_HOURS WHERE name='Skynoodle' AND Branch='Glyburide' ")

    return render(request, "jadwal_resto.html", {"schedules" : res, "total": len(res)})


def get_schedule_form(request):
    return render(request, "create_jadwal.html") 

@csrf_exempt
#@login_required(login_url="/")
def add_schedule(request):
    
    if request.method != "POST":
        return get_schedule_form(request)
    
    context = {"isNotValid" : False, "message":"Harap masukan data yang lengkap"}

    hari = request.POST["hari"]
    jam_buka = request.POST["jam_buka"]
    jam_tutup = request.POST["jam_tutup"]

    context["isNotValid"] = not hari or  not jam_buka or not jam_tutup

    if(context["isNotValid"]):
        return render(request, "create_jadwal.html", context)
    
    res = query(f"INSERT INTO RESTAURANT_OPERATING_HOURS VALUES ('Skynoodle', 'Glyburide', '{hari}', '{jam_buka}', '{jam_tutup}')")

    return redirect("/jadwal")

@csrf_exempt
def update_schedule(request, oldDay):

    res = query(f"SELECT * FROM RESTAURANT_OPERATING_HOURS WHERE (Name, BRanch, day) = ('Skynoodle', 'Glyburide', '{oldDay}')")[0]


    if request.method != "POST":
        oldValues = {
            "old_day" : oldDay,
            "old_open" : str(res["starthours"]),
            "old_close" : str(res["endhours"]),
        }

        print(oldValues["old_open"])

        return render(request, "ubah_jadwal.html", oldValues)

    hari = request.POST.get("hari", res["day"])
    jam_buka = request.POST["jam_buka"]
    jam_tutup = request.POST["jam_tutup"]

    res = query(f"UPDATE RESTAURANT_OPERATING_HOURS SET starthours='{jam_buka}',endhours='{jam_tutup}' WHERE (Name, Branch, day) = ('Skynoodle', 'Glyburide', '{hari}')")

    return redirect("/restopay/jadwal")

def delete_schedule(request, hari):
    query(f"DELETE FROM RESTAURANT_OPERATING_HOURS WHERE (Name, Branch, day) = ('Skynoodle', 'Glyburide', '{hari}')")

    return redirect("/restopay/jadwal")

@csrf_exempt
def get_all_transaction(request):
    
    
    res = query(f"SELECT * FROM USER_ACC JOIN (SELECT * FROM TRANSACTION_HISTORY TH JOIN TRANSACTION_STATUS TS ON TH.TSid=TS.id WHERE TH.Email IN (SELECT Email FROM TRANSACTION_FOOD WHERE (RName, Rbranch) = ('Skynoodle', 'Glyburide'))) X USING(email)")
    
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_pesanan": res}

    return render(request, "list_pesanan.html", context)

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

def get_ongoing_pesanan(request):
    
    res = query(f"SELECT * FROM USER_ACC JOIN (SELECT * FROM TRANSACTION_HISTORY TH JOIN TRANSACTION_STATUS TS ON TH.TSid=TS.id WHERE TH.Email IN (SELECT Email FROM TRANSACTION_FOOD WHERE (RName, Rbranch) = ('Skynoodle', 'Glyburide')) AND (TS.name ILIKE 'pending' OR TS.name ILIKE 'on%')) X USING(email)") 
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_pesanan": res}

    return render(request, "ongoing_pesanan.html", context)

@csrf_exempt
def update_transaction(request):
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

    return redirect('/restopay/pesanan/ongoing')
        