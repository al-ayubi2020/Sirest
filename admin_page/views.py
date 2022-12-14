from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from utils.query import query
from landing_page.views import is_authenticated, get_role, get_role_email
from datetime import datetime

def index(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    email = request.session["email"]

    admin_query = query(
        f"select * from user_acc WHERE email = '{email}'"
        )

    thisdict = []

    for data in admin_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4]})

    transaction_actor_query = query(
        f"select * from transaction_actor natural join user_acc"
        )

    transaction_actor_dict = []

    for data in transaction_actor_query:
        transaction_actor_dict.append({'email': data[0], 'role': get_role_email(data[0]), 'fname': data[8], 'lname': data[9], 'adminid': data[5]})

    return render(request, 'index_admin_page.html', {'data': thisdict[0], 'list': transaction_actor_dict})

@csrf_exempt
def kategori_restoran(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    if request.method == 'POST':
        nama_kategori = request.POST.get('category_name')
        kategori_restoran_query = query("select * from restaurant_category")

        last_id = ""
        for kategori in kategori_restoran_query:
            last_id = str(kategori[0])
        id_num = int(last_id[2:]) + 1

        id_baru = "RC" + str( id_num )
        query(f"insert into restaurant_category values ('{id_baru}', '{nama_kategori}')")

    kategori_restoran_query = query("select * from restaurant_category")
    kategori_restoran_query_dict = []

    for kategori in kategori_restoran_query:
        jumlah_refer_query = query(f"select count(*) from restaurant where rcategory = '{kategori[0]}'")
        for jumlah_refer in jumlah_refer_query:
            kategori_restoran_query_dict.append({'id': kategori[0], 'nama': kategori[1], 'jumlah_refer': jumlah_refer[0]})

    context = {
        'list_kategori': kategori_restoran_query_dict,
    }

    return render(request, 'kategori_restoran.html', context)

def hapus_kategori_restoran(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    query(f"delete from restaurant_category where id = '{id}'")
    return redirect("admin_page:kategori_restoran")

def form_bahan_makanan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    if request.method == 'POST':
        nama_baru = request.POST.get('bahan_name')
        qqueryy = query("select * from ingredient")

        last_id = ""
        for i in qqueryy:
            last_id = str(i[0])
        id_num = int(last_id[1:]) + 1
        id_new = f'I{str(id_num)}'
        query(f"insert into ingredient values ('{id_new}', '{nama_baru}')")
        return redirect('admin_page:daftar_bahan_makanan')

    return render(request, 'form_bahan_makanan.html')

def daftar_bahan_makanan(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")
    
    bahan_query = query(f"select * from ingredient")

    bahan_dict = []
    counter = 1
    for i in bahan_query:
        jumlah_refer_query = query(f"select count(*) from food_ingredient where ingredient = '{i[0]}'")
        for j in jumlah_refer_query:
            bahan_dict.append({'no': counter, 'bahan': i[1], 'jumlah_refer': int(j[0]), 'id': i[0]})
        counter+=1

    context = {
        'list_bahan': bahan_dict,
    }
    return render(request, 'daftar_bahan_makanan.html', context)

def hapus_bahan_makanan(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")
    query(f"delete from ingredient where id = '{id}'")
    return redirect('admin_page:daftar_bahan_makanan')
    

def detail(request):
    if not is_authenticated(request):
        return redirect("/")
    

    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    email = request.GET.get("email")

    customer_query = query(
        f"select * from user_acc natural join transaction_actor WHERE email = '{email}'"
        )

    thisdict = []

    for data in customer_query:
        thisdict.append({'email': data[0], 'password': data[1], 'phonenum': data[2], 'fname': data[3], 'lname': data[4], 'nik': data[5], 'bankname': data[6], 'accountno': data[7], 'restopay': data[8], 'adminid': data[9]})

    return render(request, 'detail_user.html', {'data': thisdict[0]})

def acc(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    email_user = request.GET.get("email")

    email_admin = request.session["email"]
    
    acc_query = query(
        f"update transaction_actor set adminid = '{email_admin}' WHERE email = '{email_user}'"
        )

    return redirect("/admin")

def kategori(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")
    food_ingredient = query(f"SELECT * FROM food_category")
    data=list()
    for x in food_ingredient:
        data.append(x[1])
    return render(request, 'crd_kategori.html',{'data':data})

def tambah_kategori(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    return render(request, 'tambah_kategori.html')



@csrf_exempt
def tambah_kategoris(request):
    
    nama = request.POST.get("kategori")
    admin_result = query(
            f"""
            INSERT INTO food_category VALUES
            ('{1}','{nama}')
        """
        )
    print(admin_result)
    return redirect("/admin/kategori")

def tarif_pengiriman(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    list_tarif = query(f"SELECT * FROM DELIVERY_FEE_PER_KM")
    for i in range(len(list_tarif)):
        dict = {}
        dict["tarif"] = list_tarif[i][1:]
        dict["id"] = list_tarif[i][0]
        list_tarif[i] = dict
    context = {"list_tarif" : list_tarif}
    return render(request, 'tarif_pengiriman.html', context)


def tarif_pengiriman_buat(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    if(request.method == "POST"):
        tarif = query(f"SELECT * FROM DELIVERY_FEE_PER_KM")
        maxi = 0
        for data in tarif:
            maxi = max(maxi, int(data[0][4:]))
        id = maxi + 1
        id = "DFPK" + str(id)
        province = request.POST.get('province')
        motorfee = request.POST.get('tarif-motor') 
        carfee= request.POST.get('tarif-mobil')
        feedback = query(f"INSERT INTO DELIVERY_FEE_PER_KM VALUES ('{id}', '{province}', {motorfee}, {carfee})")
        if feedback == 1:
            return redirect("admin_page:tarif_pengiriman")
        elif province == '' or request.POST.get('tarif-motor') == "" or request.POST.get('tarif-mobil') == '':
            msg = "Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu."
            messages.error(request, f"{msg}")
        else:
            msg = str(feedback).split('\n')[0]
            messages.error(request, f"{msg}")
        return render(request, 'tarif_pengiriman_buat.html')

    else:
        return render(request, 'tarif_pengiriman_buat.html')


def tarif_pengiriman_update(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    tarif = query(f"SELECT * FROM DELIVERY_FEE_PER_KM WHERE id='{id}'")[0]
    context = {}
    context['id'] = tarif[0]
    context['province'] = tarif[1]
    context['motorfee'] = tarif[2]
    context['carfee'] = tarif[3]
    if(request.method == "POST"):
        feedback = query(f"UPDATE DELIVERY_FEE_PER_KM SET motorfee={request.POST.get('tarif-motor')}, carfee={request.POST.get('tarif-mobil')} WHERE id='{id}'")
        if feedback == 1:
            return redirect("admin_page:tarif_pengiriman")
        elif request.POST.get('tarif-motor') == "" or request.POST.get('tarif-mobil') == '':
            msg = "Data yang diisikan belum lengkap, silakan lengkapi data terlebih dahulu."
            messages.error(request, f"{msg}")
        else:
            msg = str(feedback).split('\n')[0]
            messages.error(request, f"{msg}")
        
        tarif = query(f"SELECT * FROM DELIVERY_FEE_PER_KM WHERE id='{id}'")[0]
        context = {}
        context['id'] = tarif[0]
        context['province'] = tarif[1]
        context['motorfee'] = tarif[2]
        context['carfee'] = tarif[3]
        return render(request, 'tarif_pengiriman_update.html', context)

    return render(request, 'tarif_pengiriman_update.html', context)

def tarif_pengiriman_delete(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    query(f"DELETE FROM DELIVERY_FEE_PER_KM WHERE id='{id}'")
    return redirect("admin_page:tarif_pengiriman")


def makanan_admin(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    resto = query("SELECT RNAME, RBRANCH, RATING FROM RESTAURANT")
    context = {}
    context['restaurant'] = []
    for data in resto:
        dic = dict()
        dic['name'] = str(data[0]) + ' ' + str(data[1])
        dic['url'] = str(data[0]) + '+' + str(data[1])
        dic['rating'] = data[2]
        context["restaurant"].append(dic)
    return render(request, "makanan_admin.html", context)

def makanan_detail_admin(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    id = id.split('+')
    context = {}
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
    return render(request, "makanan_detail_admin.html", context)

def makanan_menu_admin(request, id):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    id = id.split('+')
    context = {}
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

    return render(request, "makanan_menu_admin.html", context)

def buat_promo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    return render(request, "buat_promo_admin.html")

def form_promo_hari(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    return render(request, "form_hari_spesial.html")

def form_promo_minimum(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    return render(request, "form_minimum_transaksi.html")

def daftar_promo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    return render(request, "daftar_promo_admin.html")

def detail_promo_minimum(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    return render(request, "detail_minimum_promo_admin.html")

def detail_promo_hari(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    return render(request, "detail_hari_promo_admin.html")
    
def ubah_promo(request):
    if not is_authenticated(request):
        return redirect("/")
    
    if not get_role(request.session["email"], request.session["password"]) == "admin":
        return redirect("/")

    return render(request, "form_ubah_promosi_admin.html")
