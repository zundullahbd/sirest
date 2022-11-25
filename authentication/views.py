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
            return redirect("/admin")
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

def get_role(email, password):
    admres = query(f"SELECT * FROM ADMIN WHERE EMAIL='{email}'AND password = '{password}")
    if type(admres) == list and len(admres) > 0:
        return 'admin'
    
    restres = query(f"SELECT * FROM RESTAURANT WHERE EMAIL='{email}'AND password = '{password}")
    if type(restres) == list and len(restres) > 0:
        return 'restoran'
    
    kurres = query(f"SELECT * FROM COURIER WHERE EMAIL='{email}'AND password = '{password}")
    if type(kurres) == list and len(kurres) > 0:
        return 'kurir'
    
    pelres = query(f"SELECT * FROM PELANGGAN WHERE EMAIL='{email}'AND password = '{password}")
    if type(pelres) == list and len(pelres) > 0:
        return 'pelanggan'




@csrf_exempt
def login(request):
    next = request.GET.get("next")
    cont = {}

    if request.method != "POST":
        return login_view(request)

    if verify(request):
        username = str(request.session["username"])
        password = str(request.session["password"])
    else:
        username = str(request.POST["username"])
        password = str(request.POST["password"])

    if not username or not password :
        cont["berhasil"] = True
        return render(request, "login.html", cont)

    role = get_role(username, password)

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
            return redirect(next)
        else:
            if role == "admin":
                return redirect("/admin_homepage/")
            elif role == "restoran":
                return redirect("/restoran_homepage/")
            elif role == "kurir":
                return redirect("/kurir_homepage/")
            elif role == "pelanggan":
                return redirect("/pelanggan_homepage/")

                

def login_view(request):
    if verify(request):
        return render(request, "login.html")


def logout(request):
    next=request.GET.get("next")
    if not verify(request):
        return redirect("auth/login/")
    request.session.flush()
    request.session.clear_expired()
    if next!= None and next!="None":
        return redirect(next)
    return redirect(" ")

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
    if request.method != "POST":
        return render(request, 'form_register_kurir.html')
    else:
        nama = str(request.POST["nama"])
        email = str(request.POST["email"])
        password = str(request.POST["password"])
        no_telp = str(request.POST["no_telp"])
        alamat = str(request.POST["alamat"])
        if not nama or not email or not password or not no_telp or not alamat:
            return render(request, 'form_register_kurir.html')
        else:
            query(f"INSERT INTO COURIER (NAMA, EMAIL, PASSWORD, NO_TELP, ALAMAT) VALUES ('{nama}', '{email}', '{password}', '{no_telp}', '{alamat}')")
            return redirect("/auth/login")