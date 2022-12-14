from django.urls import path
from .views import index, konfirmasi, kirim
from .views import restopay
from .views import isi_saldo
from .views import tarik_saldo
from .views import daftar_jam_oprasional
from .views import buat_jam_oprasional
from .views import edit_jam_oprasional
from .views import daftar_pesanan_berlangsung_restoran
from .views import ringkasan_pesanan_restoran
from .views import makanan_delete, makanan_buat, makanan_update, makanan
from .views import riwayat_pesanan_restoran, detail_pesanan
from .views import daftar_promo_tersedia, daftar_promo_restoran, form_promo_resto, detail_promo, ubah_promo, hapus_jam_oprasional




app_name = 'restoran_page'

urlpatterns = [
    path('', index, name='index'),
    path('restopay/', restopay, name='restopay'),
    path('restopay/isi/', isi_saldo, name='isi_saldo'),
    path('restopay/tarik/', tarik_saldo, name='tarik_saldo'),
    path('daftar-jam-oprasional/', daftar_jam_oprasional, name='daftar_jam_oprasional'),
    path('daftar-jam-oprasional/buat/', buat_jam_oprasional, name='buat_jam_oprasional'),
    path('daftar-jam-oprasional/edit/', edit_jam_oprasional, name='edit_jam_oprasional'),
    path('daftar-jam-oprasional/hapus/', hapus_jam_oprasional, name='hapus_jam_oprasional'),
    path('pesanan-berlangsung/', daftar_pesanan_berlangsung_restoran, name='daftar_pesanan_berlangsung_restoran'),
    path('pesanan-berlangsung/konfirmasi/', konfirmasi, name='konfirmasi'),
    path('pesanan-berlangsung/kirim/', kirim, name='kirim'),
    path('pesanan-berlangsung/ringkasan/', ringkasan_pesanan_restoran, name='ringkasan_pesanan_restoran'),
    path('makanan', makanan, name='makanan'),
    path('makanan/buat', makanan_buat, name='makanan_buat'),
    path('makanan/edit/<str:id>', makanan_update, name='makanan_update'),
    path('makanan/delete/<str:id>', makanan_delete, name='makanan_delete'),
    path('pesanan/riwayat', riwayat_pesanan_restoran, name='riwayat_pesanan_restoran'),
    path('pesanan/riwayat/detail/<str:email>/<str:datetime>/', detail_pesanan, name="detail_pesanan"),
    path('promo/daftar-promo-tersedia', daftar_promo_tersedia, name="daftar_promo_tersedia"),
    path('promo/daftar-promo-restoran', daftar_promo_restoran, name="daftar_promo_restoran"),
    path('promo/tambah_promo', form_promo_resto, name="form_promo_resto"),
    path('promo/daftar-promo-restoran/ubah', ubah_promo, name="ubah_promo"),
    path('promo/daftar-promo-restoran/detail/<str:id>', detail_promo, name="detail_promo"),
]