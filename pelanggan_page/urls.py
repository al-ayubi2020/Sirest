from django.urls import path
from .views import index
from .views import restopay
from .views import pemesanan
from .views import isi_saldo
from .views import tarik_saldo
from .views import form_alamat
from .views import pesan
from .views import pesan2
from .views import konfirmasi
from .views import ringkasan
from .views import pesanan_berlangsung
from .views import makanan_pelanggan, makanan_detail_pelanggan, makanan_menu_pelanggan
from .views import riwayat_pesanan_pelanggan, detail_pesanan, show_form_penilaian

app_name = 'pelanggan_page'

urlpatterns = [
    path('', index, name='index'),
    path('restopay/', restopay, name='restopay'),
    path('restopay/isi/', isi_saldo, name='isi_saldo'),
    path('restopay/tarik/', tarik_saldo, name='tarik_saldo'),
    path('pemesanan/', pemesanan, name='pemesanan'),
    path('form_alamat/', form_alamat, name='form_alamat'),
    path('pesan/', pesan, name='pesan'),
    path('pesan2/', pesan2, name='pesan2'),
    path('konfirmasi/', konfirmasi, name='konfirmasi'),
    path('ringkasan/', ringkasan, name='ringkasan'),
    path('pesanan_berlangsung/', pesanan_berlangsung, name='pesanan_berlangsung'),
    path('makanan', makanan_pelanggan, name="makanan_pelanggan"),
    path('makanan/detail/<str:id>', makanan_detail_pelanggan, name='makanan_detail_pelanggan'),
    path('makanan/menu/<str:id>', makanan_menu_pelanggan, name='makanan_menu_pelanggan'),
    path('pesanan/riwayat', riwayat_pesanan_pelanggan, name='riwayat_pesanan_pelanggan'),
    path('pesanan/riwayat/detail/<str:email>/<str:datetime>/', detail_pesanan, name="detail_pesanan"),
    path('pesanan/riwayat/nilai', show_form_penilaian, name="show_form_penilaian"),
    path('makanan/menu', makanan_menu_pelanggan, name='makanan_menu_pelanggan'),    
]
