from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from utils.query import query
from landing_page.views import is_authenticated, get_role
from datetime import datetime

def index(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join customer WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'birthdate': data[10], 'sex': data[11]})

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'index_pelanggan_page.html', {'data': thisdict[0], 'verify': verify})

def restopay(request):
    if not is_authenticated(request):
        return redirect("/")

    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]
    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'restopay_pelanggan.html', {'data': customer_query[0], 'verify': verify})

@csrf_exempt
def isi_saldo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]

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

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'isi_saldo_pelanggan.html', {'data': customer_query[0], 'verify': verify})

@csrf_exempt
def tarik_saldo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]

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

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'tarik_saldo_pelanggan.html', {'data': customer_query[0], 'verify': verify})

def pemesanan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'pemesanan.html', {'verify': verify})

def form_alamat(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]
    
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'form_alamat.html', {'verify': verify})

def pesan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]
    
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'pesan.html', {'verify': verify})


@csrf_exempt
def pesan2(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")


    ikan_bakar = request.POST.get("ikan_Bakar")
    ice_cream = request.POST.get("ice_cream")
    ayam_goreng = request.POST.get("ayam_goreng")
    kendaraan = request.POST.get("kendaraan")
    b_kendaraan = 20000
    
    if kendaraan =="Motor":
        b_kendaraan=10000
    metode_pembayaran = request.POST.get("metode_pembayaran")
    data=list()
    total=0
    if ikan_bakar != None:
        p = request.POST.get("c_ikan_bakar")
        if p == None:
            p=""
        data.append({"nama":"Ikan Bakar","harga":20000,"jumlah":ikan_bakar,"total":20000*int(ikan_bakar)})
        total+=20000*int(ikan_bakar)
    if ice_cream != None:
        p = request.POST.get("c_ice_cream")
        if p == None:
            p=""
        data.append({"nama":"Ice Cream","harga":5000,"jumlah":ice_cream,"total":5000*int(ice_cream)})
        total+=5000*int(ice_cream)
    if ayam_goreng != None:
        p = request.POST.get("c_ayam_goreng")
        if p == None:
            p=""
        data.append({"nama":"Ayam Goreng","harga":15000,"jumlah":ayam_goreng,"total":15000*int(ayam_goreng)})
        total+=15000*int(ayam_goreng)
    totals=total+b_kendaraan

    email = request.session["email"]
    
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'pesan2.html',{'data': data,"pengantaran":kendaraan,"b_kendaraan":b_kendaraan,"metode_pembayaran":metode_pembayaran,"total":total,"totals":totals, 'verify': verify})

def konfirmasi(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]
    
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'konfirmasi.html' ,{'verify': verify})

def ringkasan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]
    
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'ringkasan.html',{'verify': verify})

def pesanan_berlangsung(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]
    
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'pesanan_berlangsung.html',{'verify': verify})

def makanan_pelanggan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join customer WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'birthdate': data[10], 'sex': data[11]})

    email = request.session["email"]
    
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    context = {'verify': verify}
    context['data'] = thisdict[0] 
    resto = query("SELECT RNAME, RBRANCH, RATING FROM RESTAURANT")
    context['restaurant'] = []
    for data in resto:
        dic = dict()
        dic['name'] = str(data[0]) + ' ' + str(data[1])
        dic['url'] = str(data[0]) + '+' + str(data[1])
        dic['rating'] = data[2]
        context["restaurant"].append(dic)

    return render(request, "makanan_pelanggan.html", context)

def makanan_detail_pelanggan(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    email = request.session["email"]

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join customer WHERE email = '{email}'"
        )

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'birthdate': data[10], 'sex': data[11]})

    id = id.split('+')
    context = {'verify': verify}
    context['data'] = thisdict[0] 
    cur_res = query(f"SELECT * FROM RESTAURANT WHERE rname='{id[0]}' AND rbranch='{id[1]}'")[0]
    kategori = query(f"SELECT NAME FROM RESTAURANT_CATEGORY WHERE id='{cur_res[9]}'")[0][0]
    jam_operasional = query(f"SELECT day, starthours, endhours FROM RESTAURANT_OPERATING_HOURS WHERE name='{id[0]}' AND branch='{id[1]}'")
    cur_promo = query(f"SELECT PID FROM RESTAURANT_PROMO WHERE RNAME='{id[0]}' AND RBRANCH='{id[1]}' AND STARTTIME<='{datetime.now()}' AND ENDTIME>='{datetime.now()}'")
    context['rname'] = id[0]
    context['rbranch'] = id[1]
    context['rphonenum'] = cur_res[3]
    context['street'] = cur_res[4]
    context['district'] = cur_res[5]
    context['city'] = cur_res[6]
    context['province'] = cur_res[7]
    context['rating'] = cur_res[8]
    context['kategori'] = kategori
    context['operasional'] = []
    for data in jam_operasional:
        cur_time = f"Buka {data[0]} dari {data[1]} sampai {data[2]}"
        context["operasional"].append(cur_time)
    
    context['promo'] = []
    for data in cur_promo:
        context['promo'].append(query(f"SELECT PROMONAME FROM PROMO WHERE ID='{data[0]}'")[0][0])

    return render(request, "makanan_detail_pelanggan.html", context)

def makanan_menu_pelanggan(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")
    
    email = request.session["email"]

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join customer WHERE email = '{email}'"
        )

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'birthdate': data[10], 'sex': data[11]})


    id = id.split('+')
    context = {'verify': verify}
    context['data'] = thisdict[0]
    context['restaurant'] = []
    foods = query(f"SELECT * FROM FOOD WHERE rname='{id[0]}' AND rbranch='{id[1]}'")
    for data in foods:
        if(data[4] == 0):
            continue
        dic = dict()
        dic['foodname'] = data[2]
        dic['description'] = data[3]
        dic['stock'] = data[4]
        dic['price'] = data[5]
        dic['kategori'] = query(f"SELECT NAME FROM FOOD_CATEGORY WHERE ID='{data[6]}'")[0][0]
        food_ingredient = query(f"SELECT ingredient FROM FOOD_INGREDIENT WHERE rname='{id[0]}' AND rbranch='{id[1]}' AND foodname='{dic['foodname']}'")
        dic['ingredient'] = ""
        first_time = True
        for data in food_ingredient:
            if not first_time:
                dic['ingredient'] += ', '
            first_time = False
            dic["ingredient"] += str(query(f"SELECT name FROM INGREDIENT WHERE id='{data[0]}'")[0][0])
        context["restaurant"].append(dic)

    email = request.session["email"]

    customer_query = query(
        f"select * from user_acc natural join transaction_actor natural join customer WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'birthdate': data[10], 'sex': data[11]})
    
    return render(request, "makanan_menu_pelanggan.html", context)

def riwayat_pesanan_pelanggan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")
    
    email = request.session["email"]

    transaksi_selesai = "TS04"
    transaksi_batal = "TS05"

    customer_query = query(
        f"""SELECT tf.rname, tf.rbranch, t.courierid, th.datetime, ts.name, t.rating, t.email
        FROM user_acc u, transaction_actor ta, customer c, transaction_history th,
        transaction_status ts WHERE u.email = '{email}' AND u.email = ta.email AND ta.email = c.email
        AND c.email = t.email AND t.email = th.email AND th.tsid = ts.id AND 
        th.datetime = t.datetime AND th.tsid = '{transaksi_selesai}' OR th.tsid = '{transaksi_batal}'"""
    )

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid
    
    thisdict = []
    nama_kurir = ""

    
    for i in range(len(customer_query)):
        kurir = query(
        f"SELECT fname, lname FROM user_acc WHERE email = '{customer_query[i][2]}'")
        nama_kurir = kurir[0][0] + " " + kurir[0][1]
        
        #thisdict.append({'rname': data[0], 'rbranch': data[1], 'nama_kurir': nama_kurir, 'waktu': data[3], 'status': data[4], 'rating': data[5]})
        #customer_query[i][2] = nama_kurir
        dic = dict()
        dic['restaurant'] = customer_query[i][0] + " " + customer_query[i][1]
        dic['kurir'] = nama_kurir
        dic['waktu'] = customer_query[i][3]
        dic['status'] = customer_query[i][4]
        dic['rating'] = customer_query[i][5]
        dic['email'] = customer_query[i][6]
    
        customer_query[i] = dic
    context['customer_query'] = customer_query

    context['verify'] = verify

    return render(request, 'riwayat_pesanan_pelanggan.html', context)

def detail_pesanan(request, email, datetime):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")
    
    email = request.session["email"]

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

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    context['verify'] = verify

    return render(request, "detail_pesanan.html", context)

def show_form_penilaian(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "customer":
        return redirect("/")

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, "form_penilaian_pesanan.html",{'verify':verify})
