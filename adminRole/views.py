from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from utils.query import query
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
import uuid

def dashAdmin(request):
    res = query(f"select TA.email, fname, lname,adminid from transaction_actor TA join user_acc U on TA.email = U.email")
    context = {
        'aktor' : res,
    } 
    return render(request, "home.html",context)


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

def get_all_tarif(request):
    temp  = query("""select row_number() over() as "row", * from delivery_fee_per_km""")
    context = {
      'tarif' : temp,
    }
    print(temp)
    return render(request, "daftarTP.html", context)

def tarif_pengiriman(request, valid=1):
    print("gagal")
    return render(request, 'formTP.html', {'valid':valid})

def add_tarif(request):
    province = request.POST["province"]
    motorfee = request.POST["motorfee"]
    carfee = request.POST["carfee"]
    print(province + " ini")

    if province == '':
        return tarif_pengiriman(request, 0)

    print(province + " ini")
    generate_id = uuid.uuid4()
    hasil = str(generate_id)
    id = hasil[0:6]
    gid = "ZYX0{}".format(id)
    quer = f"insert into delivery_fee_per_km values('{gid}','{province}','{motorfee}','{carfee}')"
    temp = query(quer)
    return get_all_tarif(request)


@csrf_exempt  
def delete_tarif(request):
  id = request.POST['id']
  res = query(f"DELETE FROM delivery_fee_per_km WHERE id='{id}'")
  return get_all_tarif(request)

def update_tarif(request, province):
    context = {}
    print(province)
    motor = request.POST.get('motor')
    car = request.POST.get('car')
    print(motor)
    quer = f"UPDATE delivery_fee_per_km SET motorfee = '{motor}', carfee = '{car}' WHERE  province = '{province}'"
    temp = query(quer)
    print(temp)

    context = {
        'provinsi' : province
    }
    
    return render(request, "updateTP.html",context)

@csrf_exempt
def cp(request):
    username = request.session['username']

    res = query(f"SELECT * FROM PROMO")


    if request.method != "POST":

        return render(request, "createPromo.html")

    p_min_transaksi = request.POST["p_min_transaksi"]
    p_hari_spesial = request.POST["p_hari_spesial"]

    return redirect("create-promo/min-transaksi.")

def fmt(request):
    res = query(f"SELECT P.PromoName, MTP.Id, SDP.Id FROM RESTAURANT_PROMO AS RP, PROMO AS P, MIN_TRANSACTION_PROMO AS MTP, SPECIAL_DAY_PROMO AS SDP WHERE RP.PId = P.Id AND RP.PId = MTP.Id AND RP.RName = 'Skynoodle' AND RP.RBranch = 'Glyburide';")
    
    for i in res:
        i['PId'] = str(i['PId'])

    context = {"total" : len(res), "list_promo": res}

    return render(request, "form_min_transaksi.html")

def fhs(request):
    res = query(f"SELECT P.PromoName, MTP.Id, SDP.Id FROM RESTAURANT_PROMO AS RP, PROMO AS P, MIN_TRANSACTION_PROMO AS MTP, SPECIAL_DAY_PROMO AS SDP WHERE RP.PId = P.Id AND RP.PId = MTP.Id AND RP.RName = 'Skynoodle' AND RP.RBranch = 'Glyburide';")
    
    for i in res:
        i['PId'] = str(i['PId'])

    context = {"total" : len(res), "list_promo": res}

    return render(request, "form_hari_spesial.html")

def detailAktor(request):
    return render(request, "profil.html")

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

def get_all_kategori_restoran(request):
    temp = query("""select row_number() over() as "row", * from restaurant_category""")
    rcid = query("select rcategory from restaurant")
    rcname = query('select name from restaurant_category')

    restaurant_category = []
    for a in rcname:
        restaurant_category.append(a['name'])
    
    restaurant = []
    for a in rcid:
        restaurant.append(a['rcategory'])
    
    context = {
        'listKategoriRes' : temp,
        'listRestaurant' : restaurant,
    }
    return render(request, 'kategori_restoran.html', context)


@csrf_exempt
def add_kategori_restoran(request):
    name = request.POST.get("nama")
    
    if name == '':
        return kategori_restoran(request, 0)
    id = uuid.uuid1()
    print(name, str(id))
    queryres = f"INSERT INTO restaurant_category VALUES('{str(id)[:20]}','{name}')"
    temp = query(queryres)

    return HttpResponseRedirect('/admin-resto/kategori_restoran/read/')

@csrf_exempt
def delete_kategori_restoran(request):
    id = request.POST['id']
    res = query(f"DELETE FROM restaurant_category WHERE id='{id}'")
    return HttpResponseRedirect('/admin-resto/kategori_restoran/read/')

@csrf_exempt
def kategori_restoran(request, valid=1):
    return render(request, "add_kategori_res.html", {'valid': valid})

# bryan DONE
def get_all_kategori_makanan(request):
    temp  = query("""select row_number() over() as "row", * from food_category""")
    fd = query("select fcategory from food")
    fc =  query('select name from food_category')

    food_category = []
    for i in fc:
        food_category.append(i['name'])

    food = []
    for i in fd:
        food.append(i['fcategory'])

    context = {
      'listKategori' : temp,
      'listFood' : food,
    }
    
    # return render(request, 'read.html', context)
    return render(request, "kategori_makanan.html", context)

# bryan DONE
def kategori_makanan(request, valid=1):
#   print('tidak masuk')
  return render(request, 'add_kategori_makanan.html', {'valid':valid})

# bryan DONE
def add_kategori_makanan(request):
    nama = request.POST.get("nama")

    if nama == '':
        return kategori_makanan(request, 0)
    id = uuid.uuid1()
    print(nama, str(id))
    quer = f"insert into food_category values('{str(id)[:12]}','{nama}')"
    temp = query(quer)
    # return JsonResponse({"instance": "Kategori Dibuat"},status=200)
    return get_all_kategori_makanan(request)

# bryan DONE
@csrf_exempt  
def delete_kategori_makanan(request):
  id = request.POST['id']

  res = query(f"DELETE FROM FOOD_CATEGORY WHERE id='{id}'")
  return get_all_kategori_makanan(request)


def get_all_bahan_makanan(request):
    temp = query("""select row_number() over() as "row", * from ingredient""")
    fid = query("select ingredient from food_ingredients")
    finame = query('select name from ingredient')
    print(fid)

    ingredient = []
    for i in finame:
        ingredient.append(i['name'])

    food_ingredient = []
    for i in fid:
        food_ingredient.append(i['ingredient'])
    
    context = {
        'listBahanMakanan' : temp,
        'listFoodIngredient' : food_ingredient,
    }
    return render(request, 'list_bahan_makanan.html', context)

@csrf_exempt
def bahan_makanan(request, valid=1):
    return render(request, "add_bhn_makanan.html", {'valid':valid})

@csrf_exempt
def add_bahan_makanan(request):
    name = request.POST.get("nama")
    if name == '':
        return bahan_makanan(request, 0)
    id = uuid.uuid1()
    print(name, str(id))
    queryres = f"INSERT INTO ingredient VALUES('{str(id)[:20]}','{name}')"
    temp = query(queryres)

    return HttpResponseRedirect('/admin-resto/bahan_makanan/read/')

@csrf_exempt
def delete_bahan_makanan(request):
    id = request.POST['id']
    res = query(f"DELETE FROM ingredient WHERE id='{id}'")
    return HttpResponseRedirect('/admin-resto/bahan_makanan/read/')
