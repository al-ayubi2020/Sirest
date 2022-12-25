from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from utils.query import query
from landing_page.views import is_authenticated, get_role
from datetime import datetime

@csrf_exempt
def index(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")

    email = request.session["email"]

    courier_query = query(
        f"select * from user_acc natural join transaction_actor natural join courier WHERE email = '{email}'"
        )

    thisdict = []

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    for data in courier_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'platenum': data[10], 'drivinglicensenum': data[11], 'vehicletype': data[12], 'vehiclebrand': data[13]})

    return render(request, 'index_kurir_page.html', {'data': thisdict[0], 'verify': verify})

@csrf_exempt
def transaksi_pesanan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")

    transaksi_pesanan_query = query("Select tf.rname, tf.rbranch, us.fname, us.lname, tr.datetime, ts.name, tr.email, ts.id from user_acc us join transaction_actor ta on us.email = ta.email join customer cu on cu.email = ta.email join transaction tr on tr.email = cu.email join transaction_food tf on tf.email = tr.email and tf.datetime = tr.datetime join transaction_history th on th.datetime = tf.datetime join transaction_status ts on ts.id = th.tsid;")

    transaksi_pesanan_dict = []
    counter = 1
    for transaksi in transaksi_pesanan_query:
        transaksi_pesanan_dict.append({'no': counter, 'restoran': transaksi[0], 'cabang': transaksi[1], 'nama_depan': transaksi[2], 'nama_belakang': transaksi[3], 'waktu': transaksi[4].strftime("%Y-%m-%d %H:%M:%S"), 'status': transaksi[5], 'email': transaksi[6], 'id_ts': transaksi[7]})
        counter += 1

    email = request.session["email"]

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    context = {
        'list_transaksi': transaksi_pesanan_dict,
        'verify': verify
    }

    return render(request, 'transaksi_pesanan.html', context)

@csrf_exempt
def ringkasan_pesanan(request, email, datetime):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")
    # return HttpResponse(datetime)
    ringkasan_pesanan_query = query(f"Select tr.datetime, us.fname, us.lname, tr.street, tr.district, tr.city, tr.province from user_acc us join transaction_actor ta on us.email = ta.email join customer cu on cu.email = ta.email join transaction tr on tr.email = cu.email join transaction_food tf on tf.email = tr.email and tf.datetime = tr.datetime join transaction_history th on th.datetime = tf.datetime join transaction_status ts on ts.id = th.tsid join food fo on fo.rname = tf.rname and fo.rbranch =tf.rbranch and fo.foodname = tf.foodname join restaurant res on fo.rname = res.rname and fo.rbranch = res.rbranch join payment_method pm on tr.pmid = pm.id join payment_status ps on ps.id = tr.psid where tr.email = '{email}' and tr.datetime = '{datetime}'")
    for i in ringkasan_pesanan_query:
        waktu = i[0]
        nama_pelanggan = f'{i[1]} {i[2]}'
        jalan_pelanggan = i[3]
        kecamatan_pelanggan = i[4]
        kota_pelanggan = i[5]
        provinsi_pelanggan = i[6]

    ringkasan_pesanan_query2 = query(f"Select tf.rname, tf.rbranch, res.street, res.district, res.city, res.province, tf.foodname, tf.amount, tf.note from user_acc us join transaction_actor ta on us.email = ta.email join customer cu on cu.email = ta.email join transaction tr on tr.email = cu.email join transaction_food tf on tf.email = tr.email and tf.datetime = tr.datetime join transaction_history th on th.datetime = tf.datetime join transaction_status ts on ts.id = th.tsid join food fo on fo.rname = tf.rname and fo.rbranch =tf.rbranch and fo.foodname = tf.foodname join restaurant res on fo.rname = res.rname and fo.rbranch = res.rbranch join payment_method pm on tr.pmid = pm.id join payment_status ps on ps.id = tr.psid where tr.email = '{email}' and tr.datetime = '{datetime}'")
    makanan, amount, notes = list(),list(),list()
    for i in ringkasan_pesanan_query2:
        restoran = i[0]
        jalan_restoran = i[1]
        kecamatan_restoran = i[2]
        kota_restoran = i[3]
        provinsi_restoran = i[4]
        makanan += [i[5]]
        amount += [i[6]]
        notes += [i[7]]


    
    ringkasan_pesanan_query3 = query(f"Select tf.amount, tf.note, (tr.totalprice - tr.deliveryfee), tr.totaldiscount, tr.deliveryfee, tr.totalprice, pm.name from user_acc us join transaction_actor ta on us.email = ta.email join customer cu on cu.email = ta.email join transaction tr on tr.email = cu.email join transaction_food tf on tf.email = tr.email and tf.datetime = tr.datetime join transaction_history th on th.datetime = tf.datetime join transaction_status ts on ts.id = th.tsid join food fo on fo.rname = tf.rname and fo.rbranch =tf.rbranch and fo.foodname = tf.foodname join restaurant res on fo.rname = res.rname and fo.rbranch = res.rbranch join payment_method pm on tr.pmid = pm.id join payment_status ps on ps.id = tr.psid where tr.email = '{email}' and tr.datetime = '{datetime}'")

    ringkasan_pesanan_query4 = query(f"Select ps.name, ts.name, tr.courierid from user_acc us join transaction_actor ta on us.email = ta.email join customer cu on cu.email = ta.email join transaction tr on tr.email = cu.email join transaction_food tf on tf.email = tr.email and tf.datetime = tr.datetime join transaction_history th on th.datetime = tf.datetime join transaction_status ts on ts.id = th.tsid join food fo on fo.rname = tf.rname and fo.rbranch =tf.rbranch and fo.foodname = tf.foodname join restaurant res on fo.rname = res.rname and fo.rbranch = res.rbranch join payment_method pm on tr.pmid = pm.id join payment_status ps on ps.id = tr.psid where tr.email = '{email}' and tr.datetime = '{datetime}'")
    print(type(ringkasan_pesanan_query))
    print(type(ringkasan_pesanan_query2))
    print(ringkasan_pesanan_query3)
    print(type(ringkasan_pesanan_query4))



    # ringkasan_pesanan_dict = []
    # counter = 0
    # for i in ringkasan_pesanan_query:
    #     for i2 in ringkasan_pesanan_query2:
    #         if counter > 0:
    #             ringkasan_pesanan_dict['makanan'] += [i2[5]]
    #             ringkasan_pesanan_dict['amount'] += [i2[6]]
    #             ringkasan_pesanan_dict['notes'] += ''

    #         else:
    #             ringkasan_pesanan_dict.append({'waktu': i[0], 'nama_pelanggan': f'{i[1]} {i[2]}', 'jalan_pelanggan': i[3], 'kecamatan_pelanggan': i[4], 'kota_pelanggan': i[5], 'provinsi_pelanggan': i[6], 'restoran': i2[0], 'jalan_restoran': i2[1], 'kecamatan_restoran': i2[2], 'kota_restoran': i2[3], 'provinsi_restoran': i2[4], 'makanan': [i2[5]], 'amount':[i2[6]], 'notes': '', 'harga_makanan': '', 'diskon': '', 'biaya_pengantaran': '', 'total_biaya': '', 'jenis_pembayaran': '', 'status_pembayaran': '', 'status_pesanan': '', 'id_kurir': ''})
    #     counter += 1
    
    # for i in ringkasan_pesanan_dict:
    #     id_kurir = i['id_kurir']

    # kurir_info_query = query(f"Select us.fname, us.lname, c.platenum, c.vehicletype, c.vehiclebrand from user_acc us join transaction_actor ta on us.email = ta.email join courier c on c.email = ta.email where c.email = '{id_kurir}'")

    # kurir_info_dict = []
    # for i in kurir_info_query:
    #     kurir_info_dict.append({'nama_kurir': f'{i[0]} {i[1]}', 'plat_nomor': i[2], 'tipe_kendaraan': i[3], 'merek': i[4]})

    email = request.session["email"]
    
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    context = {
        # 'list_ringkasan': ringkasan_pesanan_dict,
        # 'info_kurir': kurir_info_dict,
        'verify': verify
    }


    return render(request, 'ringkasan_pesanan.html', context)

@csrf_exempt
def ubah_status_pesanan(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")
    query(
        f"update transaction_status set name = 'Pesanan Selesai' where id = '{id}'"
        )
    print(482903820)
    return redirect('/kurir/transaksi_pesanan')
    
@csrf_exempt
def restopay(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")

    email = request.session["email"]
    customer_query = query(
        f"select * from transaction_actor where email = '{email}'"
        )

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'restopay_kurir.html', {'data': customer_query[0], 'verify': verify})

@csrf_exempt
def isi_saldo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
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

    return render(request, 'isi_saldo_kurir.html', {'data': customer_query[0], 'verify': verify})

@csrf_exempt
def tarik_saldo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
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

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    return render(request, 'tarik_saldo_kurir.html', {'data': customer_query[0],'verify': verify })

@csrf_exempt
def makanan_kurir(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")

    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")

    email = request.session["email"]

    courier_query = query(
        f"select * from user_acc natural join transaction_actor natural join courier WHERE email = '{email}'"
        )

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    thisdict = []

    for data in courier_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'platenum': data[10], 'drivinglicensenum': data[11], 'vehicletype': data[12], 'vehiclebrand': data[13]})

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

    

    return render(request, "makanan_kurir.html", context)

@csrf_exempt
def makanan_detail_kurir(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")

    email = request.session["email"]

    courier_query = query(
        f"select * from user_acc natural join transaction_actor natural join courier WHERE email = '{email}'"
        )

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    thisdict = []

    for data in courier_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'platenum': data[10], 'drivinglicensenum': data[11], 'vehicletype': data[12], 'vehiclebrand': data[13]})

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
    return render(request, "makanan_detail_kurir.html", context)

@csrf_exempt
def makanan_menu_kurir(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")

    email = request.session["email"]

    courier_query = query(
        f"select * from user_acc natural join transaction_actor natural join courier WHERE email = '{email}'"
        )

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    thisdict = []

    for data in courier_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9], 'platenum': data[10], 'drivinglicensenum': data[11], 'vehicletype': data[12], 'vehiclebrand': data[13]})

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

    return render(request, "makanan_menu_kurir.html", context)

@csrf_exempt
def riwayat_pesanan_kurir(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
        return redirect("/")
    
    email = request.session["email"]

    transaksi_selesai = "TS04"
    transaksi_batal = "TS05"

    courier_query = query(
        f"""SELECT tf.rname tf.rbranch, u.fname, u.lname t.datetime, ts.name, t.email
        FROM user_acc u, transaction_history th, customer c, transaction_actor ta, transaction_status ts, transaction t, transaction_food tf
        WHERE t.courierid = '{email}' AND t.email = c.email AND c.email = ta.email AND ta.email = u.email AND t.email = tf.email AND T.email = th.email
        AND th.datetime = t.datetime AND th.tsid = '{transaksi_selesai}' OR th.tsid = '{transaksi_batal}'"""
    )
    
    # thisdict = []
    # nama_pelanggan = ""
    # nama_restoran = ""
    
    for i in range(len(courier_query)):
        # kurir = query(
        # f"SELECT fname, lname FROM user_acc WHERE email = '{customer_query[i][2]}'")
        # nama_kurir = kurir[0][0] + " " + kurir[0][1]
        
        #thisdict.append({'rname': data[0], 'rbranch': data[1], 'nama_kurir': nama_kurir, 'waktu': data[3], 'status': data[4], 'rating': data[5]})
        #customer_query[i][2] = nama_kurir
        dic = dict()
        dic['restaurant'] = courier_query[i][0] + " " + courier_query[i][1]
        dic['pelanggan'] = courier_query[i][2] + " " + courier_query[i][3]
        dic['waktu'] = courier_query[i][4]
        dic['status'] = courier_query[i][5]
        dic['email'] = courier_query[i][6]
    
        courier_query[i] = dic
    context['courier_query'] = courier_query

    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid
    context['verify'] = verify

    return render(request, "riwayat_pesanan_kurir.html", context)

@csrf_exempt
def detail_pesanan(request, email, datetime):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "courier":
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

    # restaurant = {
    #     'rname' : transaction_food[0][0],
    #     'rbranch' : transaction_food[0][1]
    # }

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

    # print(status_time)
    # print(transaction_courier)
    # print(transaction_food)
    # print(transaction_restaurant)
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
    verify_query = query(
        f"select adminid from transaction_actor WHERE email = '{email}'"
        )

    verify = verify_query[0].adminid

    context['data'] = data
    context['verify'] = verify
    return render(request, "detail_pesanan_kurir.html", context)
