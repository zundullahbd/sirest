from django.shortcuts import render, redirect
from django.db import connection
from utils.query import query

from django.db import connection
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;

forms = {}
notes = {}
notes_value = {}
res_filter_final = []

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

# DONE
@csrf_exempt
def add_pesanan(request):

    if request.method != "POST":
        res = query(f"select distinct province from delivery_fee_per_km dfpk")
        return render(request, "create_pesanan.html", {'province':res}) 
    
    context = {"isNotValid" : False, "message":"Harap masukan data yang lengkap"}

    jalan = request.POST["jalan"]
    kecamatan = request.POST["kecamatan"]
    kota = request.POST["kota"]
    provinsi = request.POST["provinsi"]

    context["isNotValid"] = not jalan or not kecamatan or not kota or not provinsi

    if(context["isNotValid"]):
        return render(request, "create_pesanan.html", context)
    
    forms['street'] = jalan
    forms['district'] = kecamatan
    forms['city'] = kota
    forms['provinsi'] = provinsi

    # res = query(f"INSERT INTO RESTAURANT_OPERATING_HOURS VALUES ('{res_name}', '{r_branch}', '{jalan}', '{kecamatan}', '{kota}')")
    return redirect("/pelanggan/list_cabang")

# DONE
@csrf_exempt
def get_list_cabang(request):
    # provinsi = request.session['provinsi']
    print("provinsi",forms['provinsi'])
    res = query(f"""select row_number() over() as "row", r.rname, r.rbranch , p.promoname promo, p.discount
                    from restaurant r 
                    join restaurant_promo rp 
                        on r.rname = rp.rname and r.rbranch = rp.rbranch 
                    join promo p 
                        on p.id = rp.pid 
                    WHERE r.province = '{forms['provinsi']}'""") 

    context = {"list_resto": res}
    # print(res)
    return render(request, "pilih_cabang.html", context)

# DONE
# Asumsikan promo hanya dapat dimiliki 1 pada setiap restoran
# Promo diskon ini yang akan digunakan pada 
@csrf_exempt
def get_list_makanan(request):
    if request.method == "POST":
        rname = request.POST['rname']
        rbranch = request.POST['rbranch']
        discount = request.POST['discount']
        # print(discount)
        forms['rname']=rname
        forms['rbranch']=rbranch
        forms['discount']=discount
    else:
        rname = forms['rname']
        rbranch = forms['rbranch']

    print("rname rbranch",rname, rbranch)
    # print(request.session.keys())
    res = query(f"""select row_number() over() as "row",foodname, price
                    from restaurant r 
                    join food f 
                    using (rname,rbranch)
                    where r.rname = '{rname}' and rbranch = '{rbranch}'""") 
    # print(res)

    res2 = query("select distinct name from payment_method pm")

    return render(request, "pilih_makanan.html", {'list_food':res, 'list_payment':res2,'valid':1})

# DONE
@csrf_exempt
def add_catatan(request):
    if request.method == 'POST':
        try:
            food = request.POST['foodname']
            notes['food'] = food
            print("food", food)
        except:
            food = notes['food']
            catatan = request.POST['catatan']
            notes_value[food] =  catatan
            print('notes value', notes_value)
    return render(request, 'catatan.html')

# DONE
@csrf_exempt
def get_daftar_pesanan(request):
    # print(request.POST)
    if request.method == 'POST':
        pembayaran = request.POST['pembayaran']
        kendaraan = request.POST['kendaraan']
        forms['pembayaran'] = pembayaran
        forms['kendaraan'] = kendaraan
    rname = forms['rname']
    rbranch = forms['rbranch']
    res = query(f"""select row_number() over() as "row",foodname, price, rating
                    from restaurant r 
                    join food f 
                    using (rname,rbranch)
                    where r.rname = '{rname}' and rbranch = '{rbranch}'""") 
    res2 = query("select distinct name from payment_method pm")

    filter = []
    for i in range(1,len(res)+1):
        filter.append(int(request.POST['output'+str(i)]))
    # print(filter)

    if sum(filter)==0:
        return render(request, "pilih_makanan.html", {'list_food':res, 'list_payment':res2,'valid':0})

    res_filtered = []
    total_price = 0
    for i,j in zip(filter,res):
        if i > 0:
            j['price_cum'] = j['price']*i
            j['jumlah'] = i
            total_price+=j['price_cum']
            res_filtered.append(j)
    print("======== res filter ============")
    print(res_filtered)
    res_filter_final.extend(res_filtered)

    date = datetime.datetime.now()
    date= date.strftime("%Y-%m-%d %H:%M:%S")

    res3 = query(f"""select id from delivery_fee_per_km dfpk 
                    where province = '{forms['provinsi']}'""")
    # print(res)
    # print(res3)
    pembayaran = forms['pembayaran']
    # print(pembayaran)
    res4 = query(f"select id from payment_method pm where name = '{pembayaran}'")

    kendaraan = forms['kendaraan']
    res5 = query(f"select email from courier c where vehicletype = '{kendaraan}'")

    disc = int(forms['discount'])
    if disc > 100:
        disc = 100

    lists = {}
    # TO DO
    # lists['email'] = request.session['email']
    lists['email'] = 'arapkins8@reddit.com'
    lists['datetime'] = date
    lists['street'] = forms['street']
    lists['district'] = forms['district']
    lists['city'] = forms['city']
    lists['province'] = forms['provinsi']
    lists['totalfood'] = int(total_price)
    lists['totaldiscount'] = int((disc)/100 * total_price)
    lists['deliveryfee'] = 0
    lists['totalprice'] = 0
    lists['rating'] = int(res[0]['rating'])
    lists['pmid'] = res4[0]['id']
    lists['psid'] = 'SzKzmHaqm1'
    lists['dfid'] = res3[0]['id']
    lists['courierid'] = res5[0]['email']
    lists['vehicletype'] = kendaraan
 
    print(lists)
    res = query(f"""INSERT INTO TRANSACTION VALUES 
                    ('{lists['email']}', '{lists['datetime']}', '{lists['street']}', '{lists['district']}', 
                    '{lists['city']}', '{lists['province']}', '{lists['totalfood']}', '{lists['totaldiscount']}',
                    '{lists['deliveryfee']}', '{lists['totalprice']}', '{lists['rating']}', '{lists['pmid']}',
                    '{lists['psid']}', '{lists['dfid']}', '{lists['courierid']}', '{lists['vehicletype']}')""")

    final_res = query(f"""select *
                        from transaction t
                        order by row_number() over() desc
                        limit 1""")
    print(final_res)

    return render(request, "daftar_pesanan.html", {'list_food':res_filtered,
                                                    'pembayaran':pembayaran,
                                                    'kendaraan':kendaraan,
                                                    'total_price':total_price,
                                                    'final':final_res[0]
                                                    })

@csrf_exempt
def get_konfirmasi_pembayaran(request): 
    rname = forms['rname']
    rbranch = forms['rbranch']
    res = query(f"""select datetime::text, fname || ' ' || lname as name, 
                    t.street , t.district, t.city , t.province ,
                    r.rname || ' ' || r.rbranch restaurant, r.street rstreet, r.district rdistrict,
                    r.city rcity, r.province rprovince, t.totalfood , t.totaldiscount , 
                    t.deliveryfee ,t.totalprice , pm."name" pembayaran , ps."name" status 
                    from transaction t
                    join payment_status ps 
                    on ps.id = t.psid 
                    join payment_method pm 
                    on pm.id = t.pmid  
                    join user_acc ua 
                    on ua.email = t.email 
                    join restaurant r 
                    on r.rname = '{rname}' and r.rbranch = '{rbranch}'
                    order by datetime desc
                    limit 1""")

    for i in res_filter_final:
        food  = i['foodname']
        try:
            i['note'] = notes_value[food]
        except:
            i['note'] ='Tidak ada catatan'

    print('===========res_filter_final===============')
    print(res_filter_final)
    return render(request, "konfirmasi_pembayaran.html", {"ringkasan": res[0], 
                                                        "res_final":res_filter_final})

@csrf_exempt
def get_ringkasan_pesanan(request):
    # forms.clear()
    rname = forms['rname']
    rbranch = forms['rbranch']
    time = request.POST['time']
    print(time)
    
    res = query("""select email, datetime from "transaction" t 
                    order by 2 desc
                    limit 1""")
    email = res[0]['email']
    date = res[0]['datetime']

    print(email, date)
    if int(time) > 2:
        query("""with temp as(
                    select datetime from "transaction" t 
                    order by 1 desc
                    limit 1
                )
                UPDATE "transaction" t
                SET psid = 'vq63gaILPd'
                WHERE t.datetime = (select datetime from temp)""")
        
        query(f"""insert into transaction_history
                values('{email}','{date}','X19DBUSBDU',null)""")
    else:
        query("""with temp as(
                    select datetime from "transaction" t 
                    order by 1 desc
                    limit 1
                )
                UPDATE "transaction" t
                SET psid = 'F8LCGrKFTm'
                WHERE t.datetime = (select datetime from temp)""")
        
        query(f"""insert into transaction_history
                values('{email}','{date}','Z11SNJSHDG',null)""")

    res = query(f"""select t.datetime::text, ua.fname || ' ' || ua.lname as name, 
                    t.street , t.district, t.city , t.province ,
                    r.rname || ' ' || r.rbranch restaurant, r.street rstreet, r.district rdistrict,
                    r.city rcity, r.province rprovince, t.totalfood , t.totaldiscount , 
                    t.deliveryfee ,t.totalprice , pm."name" pembayaran , ps."name" status,
                    ua2.fname || ' ' || ua2.lname as courier_name, 
                    c.platenum , c.vehicletype , c.vehiclebrand, ts."name" as status_trx
                    from transaction t
                    join payment_status ps on ps.id = t.psid 
                    join payment_method pm on pm.id = t.pmid  
                    join user_acc ua on ua.email = t.email 
                    join restaurant r on r.rname = '{rname}' and r.rbranch = '{rbranch}'
                    join courier c on c.email = t.courierid 
                    join user_acc ua2 on ua2.email = t.courierid 
                    join transaction_history th on th.datetime = t.datetime 
                    join transaction_status ts on ts.id = th.tsid 
                    order by 1 desc limit 1""")
    print(res)

    if res[0]['status'] == 'Cancelled':
        res[0]['courier_name'] = '-'
        res[0]['platenum'] = '-'
        res[0]['vehicletype'] = '-'
        res[0]['vehiclebrand'] = '-'

    for i in res_filter_final:
        food  = i['foodname']
        try:
            i['note'] = notes_value[food]
        except:
            i['note'] ='Tidak ada catatan'

        print(f"""insert into transaction_food 
                values('{email}', '{date}', '{rname}', '{rbranch}', '{i['foodname']}', 
                        {int(i['jumlah'])}, '{i['note']}')""")
        query(f"""insert into transaction_food 
                values('{email}', '{date}', '{rname}', '{rbranch}', '{i['foodname']}', 
                        {int(i['jumlah'])}, '{i['note']}')""")

    return render(request, "ringkasan_pesanan.html",{"ringkasan": res[0], 
                                                        "res_final":res_filter_final})

def get_ongoing_pesanan(request):
    # res_name = request.session['rname']
    # r_branch = request.session['rbranch']

    # TO DO
    email =  'arapkins8@reddit.com'
    res = query(f"""select distinct tf.rname || ' '  || tf.rbranch as restaurant, t.datetime, ts."name" 
                    from "transaction" t
                    join transaction_history th 
                    on t.email = th.email and t.datetime = th.datetime 
                    join transaction_status ts 
                    on ts.id = th.tsid 
                    join transaction_food tf 
                    ON tf.email = t.email  and tf.datetime = t.datetime 
                    where t.email = 'arapkins8@reddit.com' and ts."name" = 'Pending'""") 
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_pesanan": res, 'email': email}

    return render(request, "ongoing_pelanggan.html", context)


@csrf_exempt
def get_transaction_detail(request):
    if request.method == "POST":
        email = request.POST["email"]
        time = request.POST["time"]

        print(email, time)
        foods = query(f"""select rname, rbranch, foodname, amount, note
                    from "transaction" t
                    join transaction_food tf 
                    on t.email = tf.email and t.datetime = tf.datetime 
                    where t.email='{email}' and t.datetime = '{time}'""")
        
        # print(foods)
        res = query(f"""select t.datetime::text, ua.fname || ' ' || ua.lname as name, 
                    t.street , t.district, t.city , t.province ,
                    r.rname || ' ' || r.rbranch restaurant, r.street rstreet, r.district rdistrict,
                    r.city rcity, r.province rprovince, t.totalfood , t.totaldiscount , 
                    t.deliveryfee ,t.totalprice , pm."name" pembayaran , ps."name" status,
                    ts."name" as status_trx, ua2.fname || ' ' || ua2.lname as courier_name, 
                    c.platenum , c.vehicletype , c.vehiclebrand
                    from transaction t
                    join payment_status ps 
                    on ps.id = t.psid 
                    join payment_method pm 
                    on pm.id = t.pmid  
                    join user_acc ua 
                    on ua.email = t.email 
                    join restaurant r 
                    on r.rname = '{foods[0]['rname']}' and r.rbranch = '{foods[0]['rbranch']}'
                    join courier c 
                    on c.email = t.courierid 
                    join user_acc ua2 
                    on ua2.email = t.courierid 
                    join transaction_history th 
                    on th.datetime = t.datetime 
                    join transaction_status ts 
                    on ts.id = th.tsid 
                    where t.datetime = '{time}' and t.email = '{email}'""")

        print(res[0])
        return render(request, "detail_pesanan_pelanggan.html", {'list_food':foods,
                                                    'ringkasan':res[0]})

def detailRestauran(request):
    return render(request, "detailRestauran.html")

def get_transaction_history_pelanggan(request):
    
    res = query(f"SELECT R.RName, U.FName, U.LName, TH.DatetimeStatus, TS.Name, R.Rating FROM FROM RESTAURANT AS R, USER_ACC AS U, TRANSACTION_HISTORY AS TH, TRANSACTION_STATUS AS TS, COURIER AS C, TRANSACTION_ACTOR AS TA, FOOD AS F, TRANSACTION_FOOD AS TF, TRANSACTION AS T, CUSTOMER AS C WHERE TA.Email = U.Email AND C.Email = TA.Email AND R.Email = TA.Email AND F.RName = R.RName AND F.RBranch = R.RBranch AND TF.RName = F.RName AND TF.RBranch = F.RBranch AND TH.Email = T.Email AND TH.Datetime = TF.Datetime AND TH.TSId = TS.Id AND U.FName = 'Ara' AND U.LName = 'Rapkins'") 
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_transaction_history_pelanggan": res}

    return render(request, "listTransactionHistoryPelanggan.html", context)
