# User Service - Full-Stack Application

Aplikasi layanan pengguna full-stack yang dibangun dengan Flask (backend) dan HTML/CSS/JavaScript (frontend) untuk manajemen pengguna.

## Fitur

- **Backend (Flask + SQLAlchemy)**:
  - API RESTful untuk operasi CRUD (Create, Read, Update, Delete) pengguna.
  - Model pengguna dengan atribut: nama, email, tipe_pengguna (customer, driver, admin), password (di-hash).
  - Database SQLite untuk penyimpanan data.
  - Validasi input dan hashing password menggunakan SHA-256.

- **Frontend (HTML/CSS/JS)**:
  - Antarmuka web untuk manajemen pengguna.
  - Formulir untuk membuat dan mengedit pengguna.
  - Tabel untuk menampilkan daftar pengguna.
  - Interaksi dengan API backend menggunakan Fetch API.

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

- `GET /users` - Ambil semua pengguna
- `POST /users` - Buat pengguna baru
- `GET /users/<id>` - Ambil pengguna berdasarkan ID
- `PUT /users/<id>` - Perbarui pengguna berdasarkan ID
- `DELETE /users/<id>` - Hapus pengguna berdasarkan ID

## Penggunaan

1. Buka halaman frontend di browser.
2. Gunakan formulir untuk menambah pengguna baru.
3. Klik tombol "Edit" di tabel untuk mengedit pengguna.
4. Klik tombol "Hapus" untuk menghapus pengguna.
5. Data akan disimpan di database SQLite (`users.db` di folder backend).

## Teknologi yang Digunakan

- **Backend:** Flask, Flask-SQLAlchemy, Flask-CORS
- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **Database:** SQLite
- **Keamanan:** Hashing password dengan SHA-256

## Lisensi

Proyek ini dibuat untuk tujuan pembelajaran dan demonstrasi.
