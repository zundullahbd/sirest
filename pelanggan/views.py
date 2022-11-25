from django.shortcuts import render, redirect
from django.db import connection
from utils.query import query

def pelangganHome(request):
    return render(request, 'pelanggan.html')
def dMenu(request):
    return render(request, "daftarMenu.html")

def dRestauran(request):
    return render(request, "daftarRestauran.html")

def detailRestauran(request):
    return render(request, "detailRestauran.html")

def get_transaction_history_pelanggan(request):
    
    res = query(f"SELECT R.RName, U.FName, U.LName, TH.DatetimeStatus, TS.Name, R.Rating FROM FROM RESTAURANT AS R, USER_ACC AS U, TRANSACTION_HISTORY AS TH, TRANSACTION_STATUS AS TS, COURIER AS C, TRANSACTION_ACTOR AS TA, FOOD AS F, TRANSACTION_FOOD AS TF, TRANSACTION AS T, CUSTOMER AS C WHERE TA.Email = U.Email AND C.Email = TA.Email AND R.Email = TA.Email AND F.RName = R.RName AND F.RBranch = R.RBranch AND TF.RName = F.RName AND TF.RBranch = F.RBranch AND TH.Email = T.Email AND TH.Datetime = TF.Datetime AND TH.TSId = TS.Id AND U.FName = 'Ara' AND U.LName = 'Rapkins'") 
    for i in res:
        i['datetime'] = str(i['datetime'])

    context = {"total" : len(res), "list_transaction_history_pelanggan": res}

    return render(request, "listTransactionHistoryPelanggan.html", context)