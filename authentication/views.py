from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;


def login_form(request):
    return render(request, 'login.html')

def verify(uname, passw):
    res = query(f"SELECT * FROM USER_ACC WHERE email='{uname}'")

    return (len(res) != 0 and res[0]['password'] == passw)

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
    if request.method != 'POST':
        return login_form(request)
    
    email = request.POST['email']
    passwd  = request.POST['password']

    if(email is None or email == '' or passwd is None or passwd == ''):
        return render(request, 'login.html', {'invalid' : True})

    if (not verify(email, passwd)):
        return render(request, 'login.html', {'incorrect_cred' : True})
    
    role = get_role(email)
    request.session['email'] = email
    
    if (role == 'restaurant'):
        res = query(f"SELECT * FROM restaurant WHERE EMAIL='{email}'")[0]
        request.session['rname'] = res['rname']
        request.session['rbranch'] = res['rbranch']
        return redirect("/restoran")
        
    return redirect("/kemana-gatau-gan") 