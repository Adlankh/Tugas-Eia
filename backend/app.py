from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required
from models import db, User
from auth import admin_required, login_required_json
import hashlib

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Mengizinkan CORS untuk semua origins
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Ganti dengan kunci rahasia yang aman
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'pesan': 'Email dan password diperlukan'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == hash_password(data['password']) and user.is_admin():
        login_user(user)
        return jsonify({'pesan': 'Login berhasil', 'user': user.to_dict()}), 200
    return jsonify({'pesan': 'Email, password salah, atau bukan admin'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'pesan': 'Logout berhasil'}), 200

@app.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.is_admin():
            return jsonify({'authenticated': True, 'user': user.to_dict()}), 200
    return jsonify({'authenticated': False}), 401

@app.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    users = User.query.all()
    return jsonify({'pesan': 'Daftar pengguna berhasil diambil', 'data': [user.to_dict() for user in users]})

@app.route('/users', methods=['POST'])
@login_required
@admin_required
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('nama', 'email', 'tipe_pengguna', 'password')):
        return jsonify({'pesan': 'Data tidak lengkap'}), 400
    if data['tipe_pengguna'] not in ['customer', 'driver', 'admin']:
        return jsonify({'pesan': 'Tipe pengguna tidak valid'}), 400
    hashed_pw = hash_password(data['password'])
    new_user = User(nama=data['nama'], email=data['email'], tipe_pengguna=data['tipe_pengguna'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'pesan': 'Pengguna berhasil dibuat', 'data': new_user.to_dict()}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'pesan': 'Pengguna tidak ditemukan'}), 404
    return jsonify({'pesan': 'Detail pengguna berhasil diambil', 'data': user.to_dict()})

@app.route('/users/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'pesan': 'Pengguna tidak ditemukan'}), 404
    data = request.get_json()
    if 'nama' in data:
        user.nama = data['nama']
    if 'email' in data:
        user.email = data['email']
    if 'tipe_pengguna' in data and data['tipe_pengguna'] in ['customer', 'driver', 'admin']:
        user.tipe_pengguna = data['tipe_pengguna']
    if 'password' in data:
        user.password = hash_password(data['password'])
    db.session.commit()
    return jsonify({'pesan': 'Pengguna berhasil diperbarui', 'data': user.to_dict()})

@app.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'pesan': 'Pengguna tidak ditemukan'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'pesan': 'Pengguna berhasil dihapus'})

if __name__ == '__main__':
    app.run(debug=True)
