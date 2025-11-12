from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# === Konfigurasi Flask ===
app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})

# === Konfigurasi Database SQLite ===
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# === Model Tabel User ===
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tipe_pengguna = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# === Buat database (jika belum ada) ===
with app.app_context():
    db.create_all()

# === ROUTE GET SEMUA USER ===
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    data = [
        {
            "id": u.id,
            "nama": u.nama,
            "email": u.email,
            "tipe_pengguna": u.tipe_pengguna,
        }
        for u in users
    ]
    return jsonify(data), 200

# === ROUTE TAMBAH USER ===
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not all(k in data for k in ("nama", "email", "password", "tipe_pengguna")):
        return jsonify({"pesan": "Data tidak lengkap"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"pesan": "Email sudah terdaftar"}), 400

    new_user = User(
        nama=data["nama"],
        email=data["email"],
        password=data["password"],
        tipe_pengguna=data["tipe_pengguna"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"pesan": "Pengguna berhasil disimpan"}), 201

# === ROUTE UPDATE USER ===
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"pesan": "Pengguna tidak ditemukan"}), 404

    user.nama = data.get("nama", user.nama)
    user.email = data.get("email", user.email)
    user.tipe_pengguna = data.get("tipe_pengguna", user.tipe_pengguna)
    user.password = data.get("password", user.password)
    db.session.commit()

    return jsonify({"pesan": "Data pengguna diperbarui"}), 200

# === ROUTE HAPUS USER ===
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"pesan": "Pengguna tidak ditemukan"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"pesan": "Pengguna berhasil dihapus"}), 200

# === ROUTE UNTUK FRONTEND ===
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# === Jalankan server ===
if __name__ == "__main__":
    app.run(debug=True, port=5001)
