from django.urls import path
from .views import index, transaksi_pesanan, ringkasan_pesanan
from .views import index
from .views import restopay
from .views import isi_saldo
from .views import tarik_saldo
from .views import makanan_kurir, makanan_detail_kurir, makanan_menu_kurir
from .views import riwayat_pesanan_kurir, detail_pesanan, ubah_status_pesanan

app_name = 'kurir_page'

urlpatterns = [
    path('', index, name='index'),
    path('transaksi_pesanan/', transaksi_pesanan, name='transaksi_pesanan'),
    path('ubah_status_pesanan/<str:id>', ubah_status_pesanan, name='ubah_status_pesanan'),
    path('ringkasan_pesanan/<str:email>/<str:datetime>', ringkasan_pesanan, name='ringkasan_pesanan'),
    path('restopay/', restopay, name='restopay'),
    path('restopay/isi/', isi_saldo, name='isi_saldo'),
    path('restopay/tarik/', tarik_saldo, name='tarik_saldo'),
    path('makanan', makanan_kurir, name="makanan_kurir"),
    path('makanan/detail/<str:id>', makanan_detail_kurir, name='makanan_detail_kurir'),
    path('makanan/menu/<str:id>', makanan_menu_kurir, name='makanan_menu_kurir'),
    path('pesanan/riwayat', riwayat_pesanan_kurir, name="riwayat_pesanan_kurir"),
    path('pesanan/riwayat/detail/<str:email>/<str:datetime>/', detail_pesanan, name='detail_pesanan')

]