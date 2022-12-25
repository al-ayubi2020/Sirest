from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from utils.query import query
from landing_page.views import is_authenticated, get_role

import datetime
import random

@csrf_exempt
def index(request):
    if not is_authenticated(request):
        return redirect("/")
        
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join restaurant join restaurant_category on rcategory = id WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'rname': data[10], 'rbranch': data[11], 'rphonenum': data[12], 'street': data[13], 'district': data[14], 'city': data[15], 'province': data[16], 'rating': data[17], 'rcategory': data[20]})

    context = {'verify': verify}
    context['operasional'] = []
    context['data'] = thisdict[0]
    jam_operasional = query(f"SELECT day, starthours, endhours FROM RESTAURANT_OPERATING_HOURS WHERE name='{context['data']['rname']}' AND branch='{context['data']['rbranch']}'")
    for data in jam_operasional:
        cur_time = f"Buka {data[0]} dari {data[1]} sampai {data[2]}"
        context["operasional"].append(cur_time)
    return render(request, 'index_restoran_page.html', context)

@csrf_exempt
def restopay(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )
        
    return render(request, 'restopay_restoran.html', {'data': customer_query[0], 'verify': verify})

@csrf_exempt
def isi_saldo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    if request.method == "POST":
        amount = int(request.POST.get("amount"))
        isi_query = query(
        f"update transaction_actor set restopay = restopay + {amount} where email = '{email}'"
        )

        if not type(isi_query) == int:
            return JsonResponse({"message": "Gagal query update"}, status=200) 

        return JsonResponse({"message": "Berhasil Register"}, status=200) 

    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    return render(request, 'isi_saldo_restoran.html', {'data': customer_query[0], 'verify': verify})

@csrf_exempt
def tarik_saldo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    if request.method == "POST":
        amount = int(request.POST.get("amount"))
        isi_query = query(
        f"update transaction_actor set restopay = restopay - {amount} where email = '{email}'"
        )

        if not type(isi_query) == int:
            return JsonResponse({"message": "Gagal query update"}, status=200) 

        return JsonResponse({"message": "Berhasil Register"}, status=200) 

    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    return render(request, 'tarik_saldo_restoran.html', {'data': customer_query[0], 'verify': verify})

@csrf_exempt
def daftar_jam_oprasional(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    resto_query = query(
        f"select * from restaurant where email = '{email}'"
        )

    rname = resto_query[0].rname
    rbranch = resto_query[0].rbranch

    buat_query = query(
        f"select * from restaurant_operating_hours where name = '{rname}' and branch = '{rbranch}'"
        )

    thisdict = []

    for data in buat_query:
        thisdict.append({'rname': data[0], 'rbranch': data[1], 'day': data[2], 'start': data[3], 'end': data[4]})

    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    return render(request, 'daftar_jam_oprasional.html', {'list':thisdict, 'data': customer_query[0], 'verify': verify})

@csrf_exempt
def buat_jam_oprasional(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    resto_query = query(
        f"select * from restaurant where email = '{email}'"
        )

    rname = resto_query[0].rname
    rbranch = resto_query[0].rbranch

    if request.method == "POST":
        day = request.POST.get("day")
        start = request.POST.get("start")
        end = request.POST.get("end")

        buat_query = query(
        f"insert into restaurant_operating_hours values ('{rname}', '{rbranch}', '{day}', '{start}', '{end}' )"
        )

        if not type(buat_query) == int:
            return JsonResponse({"message": "Gagal query update"}, status=200) 

        return JsonResponse({"message": "Berhasil Register"}, status=200) 

    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    return render(request, 'buat_jam_oprasional.html', {'data': customer_query[0], 'verify': verify})

@csrf_exempt
def edit_jam_oprasional(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    resto_query = query(
        f"select * from restaurant where email = '{email}'"
        )

    rname = resto_query[0].rname
    rbranch = resto_query[0].rbranch
    day = request.GET.get("day")

    if request.method == "POST":
        day1 = request.POST.get("day")
        start = request.POST.get("start")
        end = request.POST.get("end")

        buat_query = query(
        f"update restaurant_operating_hours set starthours = '{start}', endhours = '{end}' where name = '{rname}' and branch = '{rbranch}' and day = '{day1}'"
        )

        if not type(buat_query) == int:
            return JsonResponse({"message": "Gagal query update"}, status=200) 

        return JsonResponse({"message": "Berhasil Register"}, status=200) 

    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    return render(request, 'edit_jam_oprasional.html', {'day': day , 'data': customer_query[0], 'verify': verify})

@csrf_exempt
def hapus_jam_oprasional(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    resto_query = query(
        f"select * from restaurant where email = '{email}'"
        )

    rname = resto_query[0].rname
    rbranch = resto_query[0].rbranch
    day = request.GET.get("day")

    delete_query = query(
        f"delete from restaurant_operating_hours where name = '{rname}' and branch = '{rbranch}' and day = '{day}'"
        )

    return redirect("/restoran/daftar-jam-oprasional/")

@csrf_exempt
def daftar_pesanan_berlangsung_restoran(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    resto_info_query = query(
        f"select rname, rbranch from restaurant where email = '{email}'"
        )

    rname = resto_info_query[0].rname
    rbranch = resto_info_query[0].rbranch 
    pesanan_berlangsung_query = query(
        f"select email, datetime, tsid, fname, lname from transaction natural join transaction_food natural join transaction_history natural join user_acc where rname = '{rname}' and rbranch = '{rbranch}' and tsid <> 'TS04' and tsid <> 'TS05'"
        )

    thisdict = []

    for data in pesanan_berlangsung_query:
        thisdict.append({'email': data[0], 'datetime': data[1].strftime("%Y-%m-%d"), 'tsid': data[2], 'fname': data[3], 'lname': data[4]})

    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    return render(request, 'daftar_pesanan_berlangsung_restoran.html', {'list': thisdict, 'data':{'adminid':customer_query[0].adminid}, 'verify': verify})

@csrf_exempt
def ringkasan_pesanan_restoran(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.GET.get("email")
    datetime = request.GET.get("datetime")

    pesanan_berlangsung_query = query(
        f"""
        select fname, lname, street, district, city, province, 
        totalfood, totaldiscount, deliveryfee, totalprice,
        courierid, pm.name as pembayaran, ps.name as status,
        c.platenum, c.vehicletype, c.vehiclebrand, ts.name as trastatus,
        foodname, amount, note
        from transaction
        natural join user_acc 
        natural join transaction_food 
        natural join transaction_history
        join transaction_status ts on tsid = ts.id
        join payment_method pm on pmid = pm.id
        join payment_status ps on psid = ps.id
        left outer join courier c on courierid = c.email
        where transaction.email = '{email}' and transaction.datetime = '{datetime}'
        """
        )

    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'ringkasan_pesanan_restoran.html',{'list': pesanan_berlangsung_query[0], 'data':{'adminid':customer_query[0].adminid}, 'verify': verify})

@csrf_exempt
def konfirmasi(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.GET.get("email")
    datetime = request.GET.get("datetime")

    pesanan_berlangsung_query = query(
        f"""
        update transaction_history
        set tsid = 'TS02'
        where email = '{email}' and datetime = '{datetime}'
        """
        )

    return redirect("/restoran/pesanan-berlangsung/")

@csrf_exempt
def kirim(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.GET.get("email")
    datetime = request.GET.get("datetime")

    courier_query = query(
        f"select email from courier"
        )

    panjang = len(courier_query)
    randomNum = random.randint(0, panjang - 1)
    email_courirer = courier_query[randomNum].email

    pesanan_berlangsung_query = query(
        f"""
        update transaction_history
        set tsid = 'TS03'
        where email = '{email}' and datetime = '{datetime}'
        """
        )

    pesanan_berlangsung_query = query(
        f"""
        update transaction
        set courierid = '{email_courirer}'
        where email = '{email}' and datetime = '{datetime}'
        """
        )

    return redirect("/restoran/pesanan-berlangsung/")

@csrf_exempt
def makanan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join restaurant join restaurant_category on rcategory = id WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'rname': data[10], 'rbranch': data[11], 'rphonenum': data[12], 'street': data[13], 'district': data[14], 'city': data[15], 'province': data[16], 'rating': data[17], 'rcategory': data[20]})

    context = {'verify': verify}
    context['data'] = thisdict[0]
    list_food = query(f"SELECT * FROM FOOD WHERE RNAME='{context['data']['rname']}' AND RBRANCH='{context['data']['rbranch']}'")
    cant_delete = query(f"SELECT FOODNAME FROM TRANSACTION_FOOD WHERE RNAME='{context['data']['rname']}' AND RBRANCH='{context['data']['rbranch']}'")
    cant_delete_list = []
    for data in cant_delete:
        cant_delete_list.append(data[0])
    for i in range(len(list_food)):
        dic = dict()
        dic['rname'] = list_food[i][0]
        dic['rbranch'] = list_food[i][1]
        dic['foodname'] = list_food[i][2]
        dic['description'] = list_food[i][3]
        dic['stock'] = list_food[i][4]
        dic['price'] = list_food[i][5]
        dic['category'] = query(f"SELECT * FROM food_category WHERE id='{list_food[i][6]}'")[0][1]
        food_ingredient = query(f"SELECT ingredient FROM FOOD_INGREDIENT WHERE rname='{context['data']['rname']}' AND rbranch='{context['data']['rbranch']}' AND foodname='{dic['foodname']}'")
        dic['ingredient'] = ""
        first_time = True
        for data in food_ingredient:
            if not first_time:
                dic['ingredient'] += ', '
            first_time = False
            dic["ingredient"] += str(query(f"SELECT name FROM INGREDIENT WHERE id='{data[0]}'")[0][0])
        dic['url'] = str(list_food[i][2])
        list_food[i] = dic
        dic['is_delete'] = not(dic['foodname'] in cant_delete_list)
    context['list_food'] = list_food
    return render(request, 'makanan.html', context)

# kinda done
@csrf_exempt
def makanan_buat(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join restaurant join restaurant_category on rcategory = id WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'rname': data[10], 'rbranch': data[11], 'rphonenum': data[12], 'street': data[13], 'district': data[14], 'city': data[15], 'province': data[16], 'rating': data[17], 'rcategory': data[20]})

    context = {'verify': verify}
    context['data'] = thisdict[0]

    if request.method == "POST":
        query_food = dict()
        query_ingredient = []
        for data in request.POST:
            if "bahan" in data:
                query_ingredient.append(request.POST.get(data))
            elif "csrfmiddlewaretoken" in data:
                continue
            else:
                query_food[data] = request.POST.get(data)
        if len(query_ingredient) == 0:
            messages.error(request, "Mohon isi bahan makanan dengan lengkap")
        else:
            feedback = query(f"INSERT INTO FOOD VALUES ('{context['data']['rname']}', '{context['data']['rbranch']}', '{query_food['foodname']}', '{query_food['description']}', '{query_food['stock']}', '{query_food['harga']}', '{query_food['kategori_makanan']}')")
            if type(feedback) == int:
                for data in query_ingredient:
                    feedback = query(f"INSERT INTO FOOD_INGREDIENT VALUES ('{context['data']['rname']}', '{context['data']['rbranch']}', '{query_food['foodname']}', '{data}')")
                return redirect("restoran_page:makanan")
            else:
                messages.error(request, "Data anda tidak valid")

    ingredient = query(f"SELECT * FROM INGREDIENT")
    context['ingredient_list'] = []
    for data in ingredient:
        cur_ingredient = dict()
        cur_ingredient['id'] = data[0]
        cur_ingredient['name'] = data[1]
        context['ingredient_list'].append(cur_ingredient)
    
    category = query(f"SELECT * FROM FOOD_CATEGORY")
    context['category_list'] = []
    for data in category:
        cur_category = dict()
        cur_category['id'] = data[0]
        cur_category['name'] = data[1]
        context['category_list'].append(cur_category)

    
    return render(request, 'makanan_buat.html', context)

@csrf_exempt
def makanan_update(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")
    
    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join restaurant join restaurant_category on rcategory = id WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'rname': data[10], 'rbranch': data[11], 'rphonenum': data[12], 'street': data[13], 'district': data[14], 'city': data[15], 'province': data[16], 'rating': data[17], 'rcategory': data[20]})

    context = {'verify': verify}
    context['data'] = thisdict[0]

    if request.method == "POST":
        query_food = dict()
        query_ingredient = []
        for data in request.POST:
            if "bahan" in data:
                query_ingredient.append(request.POST.get(data))
            elif "csrfmiddlewaretoken" in data:
                continue
            else:
                query_food[data] = request.POST.get(data)
        if len(query_ingredient) == 0:
            messages.error(request, "Mohon isi bahan makanan dengan lengkap")
        else:
            feedback = query(f"UPDATE FOOD SET description='{query_food['description']}', stock='{query_food['stock']}', price='{query_food['price']}', fcategory='{query_food['kategori_makanan']}' WHERE RNAME='{context['data']['rname']}' AND RBRANCH='{context['data']['rbranch']}' AND foodname='{id}'")
            if type(feedback) == int:
                feedback = query(f"DELETE FROM FOOD_INGREDIENT WHERE RNAME='{context['data']['rname']}' AND RBRANCH='{context['data']['rbranch']}' AND FoodName='{id}'")
                for data in query_ingredient:
                    feedback = query(f"INSERT INTO FOOD_INGREDIENT VALUES ('{context['data']['rname']}', '{context['data']['rbranch']}', '{id}', '{data}')")
                return redirect("restoran_page:makanan")
            else:
                messages.error(request, "Data anda tidak valid")


    cur_food = query(f"SELECT * FROM FOOD WHERE RNAME='{context['data']['rname']}' AND RBRANCH='{context['data']['rbranch']}' AND foodname='{id}'")[0]
    
    context['rname'] = cur_food[0]
    context['rbranch'] = cur_food[1]
    context['foodname'] = cur_food[2]
    context['description'] = cur_food[3]
    context['stock'] = cur_food[4]
    context['price'] = cur_food[5]
    context['fcategory_id'] = cur_food[6]
    context['fcategory'] = query(f"SELECT * FROM food_category WHERE id='{cur_food[6]}'")[0][1]
    context['ingredient'] = []

    food_ingredient = query(f"SELECT ingredient FROM FOOD_INGREDIENT WHERE rname='{context['data']['rname']}' AND rbranch='{context['data']['rbranch']}' AND foodname='{context['foodname']}'")
    for data in food_ingredient:
        dic = dict()
        dic['id'] = data[0]
        dic['name'] = query(f"SELECT NAME FROM INGREDIENT WHERE ID='{data[0]}'")[0][0]
        context['ingredient'].append(dic)

    context['size_ingredient'] = len(context['ingredient'])

    ingredient = query(f"SELECT * FROM INGREDIENT")
    context['ingredient_list'] = []
    for data in ingredient:
        cur_ingredient = dict()
        cur_ingredient['id'] = data[0]
        cur_ingredient['name'] = data[1]
        context['ingredient_list'].append(cur_ingredient)

    category = query(f"SELECT * FROM FOOD_CATEGORY")
    context['category_list'] = []
    for data in category:
        if data[0] == context['fcategory_id']:
            continue
        cur_category = dict()
        cur_category['id'] = data[0]
        cur_category['name'] = data[1]
        context['category_list'].append(cur_category)   
 
    return render(request, 'makanan_update.html', context)

@csrf_exempt
def makanan_delete(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")
    
    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join restaurant join restaurant_category on rcategory = id WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'rname': data[10], 'rbranch': data[11], 'rphonenum': data[12], 'street': data[13], 'district': data[14], 'city': data[15], 'province': data[16], 'rating': data[17], 'rcategory': data[20]})

    context = {'verify': verify}
    context['data'] = thisdict[0]

    query(f"DELETE FROM FOOD WHERE RNAME='{context['data']['rname']}' AND RBRANCH='{context['data']['rbranch']}' AND foodname='{id}'")

    return redirect("restoran_page:makanan")

@csrf_exempt
def riwayat_pesanan_restoran(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    transaksi_selesai = "TS04"
    transaksi_batal = "TS05"

    restaurant_query = query(
        f"""SELECT t.email, t.courierid, th.datetime, ts.name 
        FROM RESTAURANT R, FOOD F, TRANSACTION_FOOD TF, TRANSACTION T, TRANSACTION_STATUS TS
        WHERE R.email = '{email}' AND R.rname = F.rname AND R.rbranch = F.rbranch 
        AND F.rname = TF.rname AND F.rbranch = TF.rbranch AND TF.email = T.email AND TH.email = T.email
        AND TH.tsid = TS.id AND TH.tsid = '{transaksi_selesai}' OR TH.tsid = '{transaksi_batal}'"""
        )

    thisdict = []

    for i in range(len(restaurant_query)):
        pelanggan = query(
        f"SELECT fname, lname FROM user_acc WHERE email = '{restaurant_query[i][0]}'")
        nama_pelanggan = pelanggan[0][0] + " " + pelanggan[0][1]

        kurir = query(
        f"SELECT fname, lname FROM user_acc WHERE email = '{restaurant_query[i][1]}'")
        nama_kurir = kurir[0][0] + " " + kurir[0][1]
        #thisdict.append({'email_pelanggan': data[0], 'email_kurir': data[1], 'waktu_pesanan': data[2], 'status_pesanan': data[3]})

        dic = dict()
        dic['pelanggan'] = nama_pelanggan
        dic['kurir'] = nama_kurir
        dic['waktu'] = restaurant_query[i][2]
        dic['status'] = restaurant_query[i][3]
        dic['email'] = restaurant_query[i][0]
    
        restaurant_query[i] = dic
    context['restaurant_query'] = restaurant_query
    context['verify'] = verify
    #courier_email = thisdict[]
    return render(request, 'riwayat_pesanan_restoran.html', context)

@csrf_exempt
def detail_pesanan(request, email, datetime):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    data = {}
    transaction_detail = query(f'''
        SELECT * FROM TRANSACTION_HISTORY AS TH
        INNER JOIN TRANSACTION AS T
        ON TH.email = T.email and TH.datetime = T.datetime
        WHERE TH.email = '{email}' and TH.datetime = '{datetime}';
    ''')[0]

    transaction_courier = query(f'''
        SELECT * FROM USER_ACC AS UA 
        INNER JOIN COURIER AS C
        ON C.email = UA.email
        WHERE C.email = '{transaction_detail[18]}';
    ''')[0]

    transaction_food = query(f'''
        SELECT TF.rname, TF.rbranch, TF.foodname, TF.amount, TF.note
        FROM transaction_food as TF
        where TF.email = '{email}' and TF.datetime = '{datetime}';
    ''')

    transaction_restaurant = query(f'''
        SELECT * from restaurant as r
        where r.rname = '{transaction_food[0][0].replace("'","''")}' and r.rbranch = '{transaction_food[0][1].replace("'","''")}' ;
    ''')[0]

    food_order = []

    for i in range(len(transaction_food)):
        food_order.append({
            'foodname' : transaction_food[i][2],
            'amount' : transaction_food[i][3],
            'notes' : transaction_food[i][4]

        })
    
    payment_status = query(f'''
        SELECT name FROM payment_status
        WHERE id = '{transaction_detail[16]}';
    ''')[0]

    transaction_status = query(f'''
        SELECT TS.name from transaction_status AS TS
        INNER JOIN TRANSACTION_HISTORY AS TH
        ON TS.id = TH.tsid
        WHERE TH.email = '{email}' and TH.datetime = '{datetime}';
    ''')[0]

    payment_method = query(f'''
        SELECT name from payment_method
        where id = '{transaction_detail[16]}';
    ''')[0]

    status_timestamp = []

    status_time = query(f'''
        SELECT TS.name , TH.datetimestatus FROM 
        TRANSACTION_HISTORY AS TH
        INNER JOIN TRANSACTION_STATUS AS TS
        ON TS.id = TH.tsid
        WHERE TH.email = '{email}' and TH.datetime = '{datetime}';

    ''')

    for i in range (len(status_time)):
        status_timestamp.append({
            "status" : status_time[i][0],
            "timestamp" : status_time[i][1]
        })

    print(transaction_detail[11])

    data['detail_transaksi']  = [{
        "waktu_pemesanan" : datetime,
        "nama_pemesan" : pemesan,
        "jalan_pemesan" : transaction_detail[6],
        "kecamatan_pemesan" : transaction_detail[7],
        "kota_pemesan" : transaction_detail[8],
        "provinsi_pemesan" : transaction_detail[9],
        "nama_cabang_restoran" : transaction_food[0][0] + " " + transaction_food[0][1],
        "jalan_restoran" : transaction_restaurant[4],
        "kecamatan_restoran" : transaction_restaurant[5],
        "kota_restoran" : transaction_restaurant[6],
        "provinsi_restoran" : transaction_restaurant[7],
        "makanan_dipesan" : food_order,
        "total_harga_makanan" : transaction_detail[13],
        "total_diskon" : transaction_detail[11],
        "biaya_pengantaran" : transaction_detail[12],
        "total_biaya" : transaction_detail[13] + transaction_detail[11] + transaction_detail[12],
        "jenis_pembayaran" : payment_method,
        "status_pembayaran" : payment_status[0],
        "status_pesanan" : transaction_status[0],
        "nama_kurir" : transaction_courier[3] + " " + transaction_courier[4],
        "plat" : transaction_courier[6],
        "jenis_kendaraan" : transaction_courier[8],
        "merk_kendaraan" : transaction_courier[9],
        "status_timestamp" : status_timestamp
    }]

    context['data'] = data

    context['verify'] = verify

    return render(request, "detail_pesanan_restoran.html", context)

@csrf_exempt
def daftar_promo_tersedia(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, "daftar_promo_tersedia.html" ,{'verify': verify})

def daftar_promo_restoran(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, "daftar_promo_restoran.html", {'verify': verify})

@csrf_exempt
def form_promo_resto(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, "form_promo_resto.html", {'verify': verify})

@csrf_exempt
def detail_promo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")
    
    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, "detail_promo_resto.html", {'verify': verify})

@csrf_exempt
def ubah_promo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "restaurant":
        return redirect("/")
    
    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, "form_ubah_promo_resto.html", {'verify': verify})
