# User Service - Full-Stack Application

Aplikasi layanan pengguna full-stack yang dibangun dengan Flask (backend) dan HTML/CSS/JavaScript (frontend) untuk manajemen pengguna.

## Fitur

- **Backend (Flask + SQLAlchemy)**:
  - API RESTful untuk operasi CRUD (Create, Read, Update, Delete) pengguna.
  - Model pengguna dengan atribut: nama, email, tipe_pengguna (customer, driver, admin), password (di-hash).
  - Database SQLite untuk penyimpanan data.
  - Validasi input dan hashing password menggunakan SHA-256.
  - **Autentikasi dan Otorisasi**: Login/logout untuk admin, sesi berbasis Flask-Login, endpoint CRUD dilindungi hanya untuk admin.

- **Frontend (HTML/CSS/JS)**:
  - Antarmuka web untuk manajemen pengguna dengan autentikasi.
  - Formulir login untuk admin.
  - Formulir untuk membuat dan mengedit pengguna (hanya setelah login).
  - Tabel untuk menampilkan daftar pengguna (hanya setelah login).
  - Interaksi dengan API backend menggunakan Fetch API, dengan penanganan sesi login.

## Struktur Proyek

```
user-service/
├── backend/
│   ├── app.py          # Aplikasi Flask utama dengan endpoint API
│   ├── models.py       # Model database untuk User
│   ├── requirements.txt # Dependensi Python
│   └── run.py          # Script untuk menjalankan server
├── frontend/
│   ├── index.html      # Halaman utama frontend
│   ├── style.css       # Styling untuk UI
│   └── script.js       # Logika JavaScript untuk interaksi API
├── TODO.md             # Daftar tugas pengembangan
└── README.md           # Dokumentasi proyek (file ini)
```

## Instalasi dan Menjalankan

### Persyaratan
- Python 3.x
- Browser web modern

### Langkah Instalasi

1. **Clone atau download repositori ini.**

2. **Install dependensi backend:**
   ```
   cd user-service/backend
   pip install -r requirements.txt
   ```

3. **Jalankan server backend:**
   ```
   python run.py
   ```
   Server akan berjalan di `http://localhost:5001`.

4. **Buka frontend:**
   Buka file `user-service/frontend/index.html` di browser web Anda.

### Endpoint API

- `POST /login` - Login admin (memerlukan email dan password)
- `POST /logout` - Logout admin
- `GET /check-auth` - Periksa status autentikasi
- `GET /users` - Ambil semua pengguna (hanya admin)
- `POST /users` - Buat pengguna baru (hanya admin)
- `GET /users/<id>` - Ambil pengguna berdasarkan ID (hanya admin)
- `PUT /users/<id>` - Perbarui pengguna berdasarkan ID (hanya admin)
- `DELETE /users/<id>` - Hapus pengguna berdasarkan ID (hanya admin)

## Penggunaan

1. Buka halaman frontend di browser.
2. Login sebagai admin menggunakan email dan password admin yang ada di database.
3. Setelah login, gunakan formulir untuk menambah pengguna baru.
4. Klik tombol "Edit" di tabel untuk mengedit pengguna.
5. Klik tombol "Hapus" untuk menghapus pengguna.
6. Klik "Logout" untuk keluar dari sesi admin.
7. Data akan disimpan di database SQLite (`users.db` di folder backend).

## Teknologi yang Digunakan

- **Backend:** Flask, Flask-SQLAlchemy, Flask-CORS, Flask-Login
- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **Database:** SQLite
- **Keamanan:** Hashing password dengan SHA-256, autentikasi sesi

## Lisensi

Proyek ini dibuat untuk tujuan pembelajaran dan demonstrasi.
