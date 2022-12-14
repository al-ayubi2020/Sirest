from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from utils.query import query

def index_beneran(request):
    return render(request, 'landing.html')

def index(request):
    return render(request, 'index_landing_page.html')

@csrf_exempt
def register_admin(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phonenum = request.POST.get("phonenum")

        user_acc_query = query(
        f"SELECT email FROM user_acc WHERE email = '{email}' AND password = '{password}'"
        )

        if type(user_acc_query) == list and len(user_acc_query):
            return JsonResponse({"message": "Email telah terdaftar"}, status=200) 

        
        user_acc_result = query(
            f"""
            INSERT INTO user_acc VALUES
            ('{email}', '{password}', '{phonenum}', '{fname}', '{lname}')
        """
        )

        if not type(user_acc_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 

        admin_result = query(
            f"""
            INSERT INTO admin VALUES
            ('{email}')
        """
        )

        if not type(admin_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 
        else:
            request.session["email"] = email
            request.session["password"] = password
            request.session["role"] = "admin"
            request.session.set_expiry(0)
            request.session.modified = True

            print(1)
            return JsonResponse({"message": "Berhasil Register"}, status=200) 
    return render(request, 'register_admin.html')

@csrf_exempt
def register_kurir(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phonenum = request.POST.get("phonenum")
        nik = request.POST.get("nik")
        bankname = request.POST.get("bankname")
        accountno = request.POST.get("accountno")
        platenum = request.POST.get("platenum")
        drivinglicensenum = request.POST.get("drivinglicensenum")
        vehicletype = request.POST.get("vehicletype")
        vehiclebrand = request.POST.get("vehiclebrand")

        user_acc_query = query(
        f"SELECT email FROM user_acc WHERE email = '{email}' AND password = '{password}'"
        )

        if type(user_acc_query) == list and len(user_acc_query):
            return JsonResponse({"message": "Email telah terdaftar"}, status=200) 

        
        user_acc_result = query(
            f"""
            INSERT INTO user_acc VALUES
            ('{email}', '{password}', '{phonenum}', '{fname}', '{lname}')
        """
        )

        if not type(user_acc_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 

        transaction_actor_result = query(
            f"""
            INSERT INTO transaction_actor VALUES
            ('{email}', '{nik}', '{bankname}', '{accountno}', 0, NULL)
        """
        )

        if not type(transaction_actor_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 

        kurir_result = query(
            f"""
            INSERT INTO courier VALUES
            ('{email}', '{platenum}', '{drivinglicensenum}', '{vehicletype}', '{vehiclebrand}')
        """
        )

        if not type(kurir_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 
        else:
            request.session["email"] = email
            request.session["password"] = password
            request.session["role"] = "courier"
            request.session.set_expiry(0)
            request.session.modified = True

            print(1)
            return JsonResponse({"message": "Berhasil Register"}, status=200) 
    return render(request, 'register_kurir.html')

@csrf_exempt
def register_restoran(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phonenum = request.POST.get("phonenum")
        nik = request.POST.get("nik")
        bankname = request.POST.get("bankname")
        accountno = request.POST.get("accountno")
        rname = request.POST.get("rname")
        rbranch = request.POST.get("rbranch")
        rphonenum = request.POST.get("rphonenum")
        street = request.POST.get("street")
        district = request.POST.get("district")
        city = request.POST.get("city")
        province = request.POST.get("province")
        rcategory = request.POST.get("rcategory")        

        user_acc_query = query(
        f"SELECT email FROM user_acc WHERE email = '{email}' AND password = '{password}'"
        )

        if type(user_acc_query) == list and len(user_acc_query):
            return JsonResponse({"message": "Email telah terdaftar"}, status=200) 

        
        user_acc_result = query(
            f"""
            INSERT INTO user_acc VALUES
            ('{email}', '{password}', '{phonenum}', '{fname}', '{lname}')
        """
        )

        if not type(user_acc_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 

        transaction_actor_result = query(
            f"""
            INSERT INTO transaction_actor VALUES
            ('{email}', '{nik}', '{bankname}', '{accountno}', 0, NULL)
        """
        )

        if not type(transaction_actor_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 

        restoran_result = query(
            f"""
            INSERT INTO restaurant VALUES
            ('{rname}', '{rbranch}', '{email}', '{rphonenum}', '{street}', '{district}', '{city}', '{province}', 0, '{rcategory}')
        """
        )

        if not type(restoran_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 
        else:
            request.session["email"] = email
            request.session["password"] = password
            request.session["role"] = "restaurant"
            request.session.set_expiry(0)
            request.session.modified = True

            print(1)
            return JsonResponse({"message": "Berhasil Register"}, status=200) 

    thisdict = []

    DELIVERY_FEE_PER_KM_query = query(
        f"SELECT * FROM DELIVERY_FEE_PER_KM"
    )

    for data in DELIVERY_FEE_PER_KM_query:
        thisdict.append({'id': data[0], 'province': data[1]})

    print(thisdict)

    thatdict = []
    restaurant_category_query = query(
        f"SELECT * FROM restaurant_category"
    )

    for data in restaurant_category_query:
        thatdict.append({'id': data[0], 'kategori': data[1]})

    print(thatdict)
    return render(request, 'register_restoran.html', {'provinsi': thisdict, 'kategori': thatdict})

@csrf_exempt
def register_pelanggan(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phonenum = request.POST.get("phonenum")
        nik = request.POST.get("nik")
        bankname = request.POST.get("bankname")
        accountno = request.POST.get("accountno")
        birthdate = request.POST.get("birthdate")
        sex = request.POST.get("sex")


        user_acc_query = query(
        f"SELECT email FROM user_acc WHERE email = '{email}' AND password = '{password}'"
        )

        if type(user_acc_query) == list and len(user_acc_query):
            return JsonResponse({"message": "Email telah terdaftar"}, status=200) 

        
        user_acc_result = query(
            f"""
            INSERT INTO user_acc VALUES
            ('{email}', '{password}', '{phonenum}', '{fname}', '{lname}')
        """
        )
        print(user_acc_result)
        if not type(user_acc_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 

        transaction_actor_result = query(
            f"""
            INSERT INTO transaction_actor VALUES
            ('{email}', '{nik}', '{bankname}', '{accountno}', 0, NULL)
        """
        )

        if not type(transaction_actor_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 

        customer_result = query(
            f"""
            INSERT INTO customer VALUES
            ('{email}', '{birthdate}', '{sex}')
        """
        )

        if not type(customer_result) == int:
            return JsonResponse({"message": "Gagal query insert"}, status=200) 
        else:
            request.session["email"] = email
            request.session["password"] = password
            request.session["role"] = "customer"
            request.session.set_expiry(0)
            request.session.modified = True

            print(1)
            return JsonResponse({"message": "Berhasil Register"}, status=200) 
    return render(request, 'register_pelanggan.html')

def is_authenticated(request):
    try:
        request.session["email"]
        return True
    except KeyError:
        return False

def get_role(email, password):
    user_acc_query = query(
        f"SELECT email FROM user_acc WHERE email = '{email}' AND password = '{password}'"
    )

    if type(user_acc_query) == list and len(user_acc_query):

        admin_query = query(
        f"SELECT email FROM admin WHERE email = '{email}'"
        )
        
        if type(admin_query) == list and len(admin_query):
            return "admin"

        kurir_query = query(
        f"SELECT email FROM courier WHERE email = '{email}'"
        )
        
        if type(kurir_query) == list and len(kurir_query):
            return "courier"
        
        customer_query = query(
        f"SELECT email FROM customer WHERE email = '{email}'"
        )

        if type(customer_query) == list and len(customer_query):
            return "customer"

        restaurant_query = query(
        f"SELECT email FROM restaurant WHERE email = '{email}'"
        )

        if type(restaurant_query) == list and len(restaurant_query):
            return "restaurant"

    else:
        return ""

def get_role_email(email):
    user_acc_query = query(
        f"SELECT email FROM user_acc WHERE email = '{email}'"
    )

    if type(user_acc_query) == list and len(user_acc_query):

        admin_query = query(
        f"SELECT email FROM admin WHERE email = '{email}'"
        )
        
        if type(admin_query) == list and len(admin_query):
            return "admin"

        kurir_query = query(
        f"SELECT email FROM courier WHERE email = '{email}'"
        )
        
        if type(kurir_query) == list and len(kurir_query):
            return "courier"
        
        customer_query = query(
        f"SELECT email FROM customer WHERE email = '{email}'"
        )

        if type(customer_query) == list and len(customer_query):
            return "customer"

        restaurant_query = query(
        f"SELECT email FROM customer WHERE email = '{email}'"
        )

        if type(restaurant_query) == list and len(restaurant_query):
            return "restaurant"

    else:
        return ""


@csrf_exempt
def login(request):

    if request.method == "POST":
    
        if is_authenticated(request):
            request.session.flush()
            request.session.clear_expired()
        
        email = request.POST.get("email")
        password = request.POST.get("password")

        role = get_role(email, password)

        if role == "":
            return JsonResponse({"message": "Akun tidak ditemukan, periksa kembali email dan password"}, status=200) 
        else:
            request.session["email"] = email
            request.session["password"] = password
            request.session["role"] = role
            request.session.set_expiry(0)
            request.session.modified = True
            return JsonResponse({"message": "Berhasil login", "role": role}, status=200) 
    return render(request, 'index_landing_page.html')

@csrf_exempt
def logout(request):

    if not is_authenticated(request):
        return redirect("/")

    request.session.flush()
    request.session.clear_expired()

    return redirect("/")



