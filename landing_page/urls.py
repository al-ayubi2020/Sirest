from django.urls import path
from .views import index
from .views import index_beneran
from .views import register_admin
from .views import register_kurir
from .views import register_pelanggan
from .views import register_restoran
from .views import logout
from .views import login


app_name = 'landing_page'

urlpatterns = [
    path('', index_beneran, name='index_beneran'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/kurir', register_kurir, name='register_kurir'),
    path('register/admin', register_admin, name='register_admin'),
    path('register/pelanggan', register_pelanggan, name='register_pelanggan'),
    path('register/restoran', register_restoran, name='register_restoran'),
]