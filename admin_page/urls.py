from django.urls import path
from .views import index, kategori_restoran, form_bahan_makanan, daftar_bahan_makanan, hapus_kategori_restoran
from .views import index
from .views import acc
from .views import detail
from .views import kategori
from .views import tambah_kategori
from .views import tambah_kategoris
from .views import detail, tarif_pengiriman, tarif_pengiriman_buat, tarif_pengiriman_update, tarif_pengiriman_delete
from .views import makanan_admin, makanan_detail_admin, makanan_menu_admin
from .views import buat_promo, form_promo_hari, form_promo_minimum, ubah_promo
from .views import daftar_promo, detail_promo_hari, detail_promo_minimum, hapus_bahan_makanan


app_name = 'admin_page'

urlpatterns = [
    path('', index, name='index'),
    path('kategori_restoran/', kategori_restoran, name='kategori_restoran'),
    path('hapus_kategori_restoran/<str:id>', hapus_kategori_restoran, name='hapus_kategori_restoran'),

    path('form_bahan_makanan', form_bahan_makanan, name='form_bahan_makanan'),
    path('daftar_bahan_makanan', daftar_bahan_makanan, name='daftar_bahan_makanan'),
    path('hapus_bahan_makanan/<str:id>', hapus_bahan_makanan, name='hapus_bahan_makanan'),

    path('detail/', detail, name='detail'),
    path('acc/', acc, name='acc'),
    path('kategori/', kategori, name='kategori'),
    path('tambah_kategori/', tambah_kategori, name='tambah_kategori'),
    path('tambah_kategoris/', tambah_kategoris, name='tambah_kategoris'),
    path('tarif-pengiriman', tarif_pengiriman, name='tarif_pengiriman'),
    path('tarif-pengiriman/buat', tarif_pengiriman_buat, name='tarif_pengiriman_buat'),
    path('tarif-pengiriman/edit/<str:id>', tarif_pengiriman_update, name='tarif_pengiriman_update'),
    path('tarif-pengiriman/hapus/<str:id>', tarif_pengiriman_delete, name='tarif_pengiriman_delete'),
    path('makanan', makanan_admin, name="makanan_admin"),
    path('makanan/detail/<str:id>', makanan_detail_admin, name='makanan_detail_admin'),
    path('makanan/menu/<str:id>', makanan_menu_admin, name='makanan_menu_admin'),
    path('promo/buat', buat_promo, name='buat_promo'),
    path('promo/buat/minimum-transaksi', form_promo_minimum, name="form_promo_minimum"),
    path('promo/buat/hari-spesial', form_promo_hari, name="form_promo_hari"),
    path('promo/daftar-promo', daftar_promo, name="daftar_promo"),
    path('promo/daftar-promo/detail-hari', detail_promo_hari, name="detail_promo_hari"),
    path('promo/daftar-promo/detail-minimum', detail_promo_minimum, name="detail_promo_minimum"),
    path('promo/ubah', ubah_promo, name="ubah_promo")
]
