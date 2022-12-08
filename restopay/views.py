from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime;
# Create your views here.


def get_restopay(request):
    username = request.session["username"];
    role = request.session['role']
    name = request.session['rname'] + " " + request.session['rbranch']
    res = query(f"SELECT RESTOPAY, bankname, accountno FROM TRANSACTION_ACTOR WHERE Email='{username}'")[0]
    restopay = '{:,}'.format( res['restopay'])
    bank = res['bankname']
    account = res['accountno']
    return render(request,"restopay.html", {"balance": restopay, "bank" : bank, 'account': account, 'role': role, 'name': name})

def get_form_restopay(request, type):
    username = request.session["username"];
    role = request.session['role']
    name = request.session['rname'] + " " + request.session['rbranch']
    res = query(f"SELECT RESTOPAY, bankname, accountno FROM TRANSACTION_ACTOR WHERE Email='{username}'")[0]
    restopay = '{:,}'.format( res['restopay'])
    bank = res['bankname']
    account = res['accountno']

    if (type == "tambah_saldo"):
        return render(request, "tambah_restopay.html", {"balance": restopay, "bank" : bank, 'account': account, 'role': role, 'name': name})
    
    return render(request, "tarik_restopay.html", {"balance": restopay, "bank" : bank, 'account': account, 'role': role, 'name': name})

@csrf_exempt
def add_restopay(request):
    role = request.session['role']
    name = request.session['rname'] + " " + request.session['rbranch']
    context = {"isNotValid" : False, "message":"input tidak valid", 'role': role, 'name': name}

    if request.method != "POST":
        return get_form_restopay(request, "tambah_saldo")
    
    nominal = str(request.POST["nominal"])

    context["isNotValid"] = not nominal or  not nominal.isdigit(); 
    username = request.session["username"];
    
    res = query(f"SELECT RESTOPAY, bankname, accountno FROM TRANSACTION_ACTOR WHERE Email='{username}'")[0]
    context['balance'] = '{:,}'.format( res['restopay'])
    context['bank']  = res['bankname']
    context['account'] = res['accountno']

    if(context["isNotValid"]):
        return render(request, "tambah_restopay.html", context)
    
    response = query(f"UPDATE TRANSACTION_ACTOR SET RESTOPAY='{nominal}' WHERE EMAIL='{username}'");
    if(response == "Jumlah saldo tidak mencukupi."):
        context["isNotValid"] = True
        context["message"] = response
        return render(request, "tambah_restopay.html", context)

    return redirect("/restopay")


@csrf_exempt
def withdraw_restopay(request):
    role = request.session['role']
    name = request.session['rname'] + " " + request.session['rbranch']
    context = {"isNotValid" : False, "message":"input tidak valid", 'role': role, 'name': name}

    if request.method != "POST":
        return get_form_restopay(request, "tarik_saldo")
    
    nominal = str(request.POST["nominal"])

    context["isNotValid"] = not nominal or  not nominal.isdigit(); 
    username = request.session["username"];
    
    res = query(f"SELECT RESTOPAY, bankname, accountno FROM TRANSACTION_ACTOR WHERE Email='{username}'")[0]
    context['balance'] = '{:,}'.format( res['restopay'])
    context['bank']  = res['bankname']
    context['account'] = res['accountno']

    if(context["isNotValid"]):
        return render(request, "tarik_restopay.html", context)
    
    nominal = int(nominal)
    response = query(f"UPDATE TRANSACTION_ACTOR SET RESTOPAY='{nominal*-1}' WHERE EMAIL='{username}'");
    print(response)

    if(type(response) != list and response != 1 ):
        context["isNotValid"] = True
        context["message"] = "jumlah saldo tidak mencukupi."
        context['balance'] = '{:,}'.format( res['restopay'])
        return render(request, "tarik_restopay.html", context)

    return redirect("/restopay")


