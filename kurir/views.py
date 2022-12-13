from django.db import connection
from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;
from django.http import HttpResponse

def kurirHome(request):
    username = request.session['username']
    print(username)
    return render(request, "kurir.html")

#def kurirHome(request):
    res = query(f"select * from courier where email = '{request.user.email}'")
    res1 = query(f"select * from transaction_actor where email = '{request.user.email}'")
    res2 = query(f"select * from user_acc uc where uc.email = '{request.user.email}'")
    admid = query(f"select a.fname, a.lname from admin a, transaction_actor ta, user_acc uc where ta.email = '{request.user.email}' AND ta.admid = a.id AND uc.email = '{request.user.email}'")
    context = {
        'email' : res[0].get('email'),
        'password' : res[0].get('password'),
        'fname, lname' : res2[0].get('fname, lname'),
        'phone' : res2[0].get('phone'),
        'nik' :res1[0].get('nik'),
        'bankname' : res1[0].get('bankname'),
        'accountno' : res1[0].get('accountno'),
        'platenum' : res[0].get('platenum'),
        'drivinglicensenum' : res[0].get('drivinglicensenum'),
        'vehicletype' : res[0].get('vehicletype'),
        'vehiclebrand' : res[0].get('vehiclebrand'),
        'verification' : admid[0].get('fname, lname'),
        'restopay' : res[0].get('restopay'),
    }
    return render(request, "kurir.html", context)

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

def riwayat_pesanan(request):
    return render(request, "riwayat_pesanan.html")

def list_pesanan_berlangsung(request):
    temp = query("""select row_number() over() as "row", TF.rname, TF.rbranch, TF.datetime, UC.fname, UC.lname, TS.name, TS.id
                    from transaction_food tf, transaction_status ts, transaction_history th, transaction t, user_acc uc, transaction_actor ta, customer c
                    where th.tsid = ts.id and tf.email = t.email and th.email = t.email and t.email = c.email
                    and c.email = ta.email and ta.email = uc.email and ts.name = 'on process'""")   
    context = {
        'listPesanan' : temp,
        
    }
    return render(request, "list_pesanan_berlangsung.html", context)


def detail_pesanan_berlangsung(request, id):
    temp = query(f"select * from transaction_status where id = '{id}'")
    temp1 = query(f"select * from transaction_history where tsid = '{id}'")
    temp2 = query(f"select tf.foodname, tf.amount, tf.note from transaction_food tf, transaction_history th where th.email = tf.email and th.tsid = '{id}'")
    temp3 = query(f"select uc.fname, uc.lname, t.street, t.district, t.city, t.province from transaction t, transaction_actor ta, customer c , user_acc uc where t.email = ta.email and ta.email = c.email and t.email = '{temp1[0].get('email')}' and c.email = uc.email")
    #temp4 = query(f"select r.rname, r.rbranch, r.street, r.district, r.city, r.province  from transaction t, transaction_actor ta, restaurant r, user_acc uc, transaction_history th where t.email = ta.email and ta.email = r.email and t.email = '{temp1[0].get('email')}' and r.email = uc.email and t.email = th.email")
    temp5 = query(f"select t.totalprice, ps.name, t.totaldiscount, t.deliveryfee from transaction t, delivery_fee_per_km dfpk, payment_status ps where t.email = '{temp1[0].get('email')}' and t.psid = ps.id and t.dfid = dfpk.id")
    temp6 = query(f"select pm.name from transaction t, payment_method pm where t.email = '{temp1[0].get('email')}' and t.pmid = pm.id")
    context = {
        'status' : temp[0].get('name'),
        'datetime' : temp1[0].get('datetime'),
        'fname' : temp3[0].get('fname'),
        'lname' : temp3[0].get('lname'),
       
        
        'foodname' : temp2[0].get('foodname'),
        'amount' : temp2[0].get('amount'),
        'note' : temp2[0].get('note'),
        'totalprice' : temp5[0].get('totalprice'),
        'paymentstatus' : temp5[0].get('name'),
        'paymentmethod' : temp5[0].get('paymentmethod'),
        'deliveryfee' : temp5[0].get('deliveryfee'),
        'totaldiscount' : temp5[0].get('totaldiscount'),
        'custstreet' : temp3[0].get('street'),
        'custdistrict' : temp3[0].get('district'),
        'custcity' : temp3[0].get('city'),
        'custprovince' : temp3[0].get('province'),
        
        
    
        'paymentmethod' : temp6[0].get('name')
    }
    return render(request, "detail_pesanan_berlangsung.html", context)




def riwayat_pesanan_kurir(request):
    return render(request, 'riwayat_pesanan_kurir.html')


