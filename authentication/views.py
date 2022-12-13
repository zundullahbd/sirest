from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;



def get_session_data(request):
    if not verify(request):
        return {}
    try:
        return {"username": request.session["username"], "role": request.session["role"]}
    except:
        return {}

def homepage(request):
    return render(request, "welcome_page.html")

def login_form(request):
    if verify(request):
        if request.session["role"] == "admin":
            return redirect("/admin-resto")
        elif request.session["role"] == "restoran":
            return redirect("/restoran")
        elif request.session["role"] == "kurir":
            return redirect("/kurir")
        elif request.session["role"] == "pelanggan":
            return redirect("/pelanggan")
    return render(request, "login.html")

def register_view(request):
    return render(request, "register.html")

@csrf_exempt
def register_form(request):
    return render(request, 'register.html')

def register_admin(request):
    return render(request, 'form_register_admin.html')

def register_kurir(request):
    return render(request, 'form_register_kurir.html')

def register_pelanggan(request):
    return render(request, 'form_register_pelanggan.html')

def register_restoran(request):
    return render(request, 'form_register_restoran.html')

def verify(request):
    try:
        request.session["username"]
        return True
    except:
        return False

def get_role(email):
    res = query(f"SELECT * FROM ADMIN WHERE EMAIL='{email}'")
    if len(res) > 0:
        return 'admin'
    
    res = query(f"SELECT * FROM customer WHERE EMAIL='{email}'")
    if len(res) > 0:
        return 'customer'
    
    res = query(f"SELECT * FROM courier WHERE EMAIL='{email}'")
    if len(res) > 0:
        return 'courier'
    res = query(f"SELECT * FROM restaurant WHERE EMAIL='{email}'")
    if len(res) > 0:
        return 'restaurant'

@csrf_exempt
def login(request):
    next = request.GET.get("next")
    cont = {}

    if request.method != "POST":
        return login_view(request)

    username=''
    password=''
    
    if verify(request):
        username = str(request.session["username"])
        password = str(request.session["password"])
    else:
        username = str(request.POST["username"])
        password = str(request.POST["password"])

    if not username or not password :
        cont["berhasil"] = True
        return render(request, "login.html", cont)

    print(username, password)
    role = get_role(username)
    print(role)
    if role == "":
        if username and password :
            cont["gagal"] = True
            return render(request, "login.html", cont)

        return login_view(request)
    else:
        request.session["username"] = username
        request.session["password"] = password
        request.session["role"] = role
        request.session.set_expiry(0)
        request.session.modified = True

        if next != None and next != "None":
            print('salah masuk')
            return redirect(next)
        else:   
            print('masuk')
            if role == "admin":
                return redirect("/admin-resto/")
            elif role == "restaurant":
                res = query(f"SELECT * FROM restaurant WHERE EMAIL='{username}'")[0]
                request.session['rname'] = res['rname']
                request.session['rbranch'] = res['rbranch']
                return redirect("/restoran/")
            elif role == "kurir":
                return redirect("/kurir/")
            elif role == "customer":
                return redirect("/pelanggan/")

                

def login_view(request):
    if not verify(request):
        return render(request, "login.html")
    else:
        return render(request, "login.html")


def logout(request):
    next=request.GET.get("next")
    if not verify(request):
        return redirect("/login/")
    request.session.flush()
    request.session.clear_expired()
    if next!= None and next!="None":
        return redirect(next)
    return redirect("/")

@csrf_exempt
def register_admin(request):
    next = request.GET.get("next")
    body = request.POST
    cont = {}
    if request.method == "POST":
        email = body.get("adminEmailInput")
        password = body.get("adminPasswordInput")
        nama = body.get("adminNamaInput")
        no_telp = body.get("adminNoHPInput")

        if not email or not password or not nama or not no_telp:
            cont["berhasil"] = True
            return render(request, "form_register_admin.html", cont)
        
        
        

        request.session["username"] = email
        request.session["password"] = password
        request.session["role"] = "admin"
        request.session.set_expiry(0)
        request.session.modified = True

        if next != None and next != "None":
            return redirect(next)
        else:
            return redirect("/admin-resto/")
    return render(request, "form_register_admin.html", cont)


@csrf_exempt            
def register_kurir(request):
    cont = {}
    if request.method != "POST":
        return render(request, 'form_register_kurir.html')
    else:
        email = request.POST.get("kurirEmailInput")
        password = request.POST.get("kurirPasswordInput")
        nama = request.POST.get("kurirNamaInput")
        no_telp = request.POST.get("kurirNoHPInput")
        nik = request.POST.get("kurirNIKInput")
        bank = request.POST.get("kurirBankInput")
        norek = request.POST.get("kurirRekInput")
        plat = request.POST.get("kurirPlatInput")
        nosim = request.POST.get("kurirSIMInput")
        kendaraan = request.POST.get("kurirKendaraanInput")
        merk = request.POST.get("kurirMerkInput")
        if not email or not password or not nama or not no_telp or not nik or not bank or not norek or not plat or not nosim or not kendaraan or not merk:
            cont["berhasil"] = True
            return render(request, "form_register_kurir.html", cont)
        query(f"INSERT INTO courier VALUES ('{email}', '{password}', '{nama}', '{no_telp}', '{nik}', '{bank}', '{norek}', '{plat}', '{nosim}', '{kendaraan}', '{merk}')")
        return redirect("/kurir/")

    