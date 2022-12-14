# Cara Menggunakan

1. Clone repositori baru tersebut ke komputer dengan perintah git clone <URL_REPOSITORI> dengan keterangan <URL_REPOSITORI> disesuaikan dengan tautan repositori yang baru saja kamu buat.

2. Masuk ke dalam repositori yang sudah kamu clone di komputermu dan buatlah sebuah virtual environment dengan perintah berikut: `python -m venv env`

3. Nyalakan virtual environment dengan perintah yang sesuai dengan jenis operating system yang kamu gunakan.

- Windows: `env\Scripts\activate.bat`

- Unix (Linux & Mac OS): `source env/bin/activate`

4. Install dependencies yang diperlukan untuk menjalankan proyek Django dengan perintah `pip install -r requirements.txt`

5. Migrate database dengan cara `python manage.py migrate`

6. Coba jalankan proyek Django yang telah kamu buat dengan perintah `python manage.py runserver` dan bukalah http://localhost:8000 di browser favoritmu untuk mengetes apakah proyek Django dapat berjalan dengan baik.
