from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User
import hashlib

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Mengizinkan CORS untuk semua origins
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'pesan': 'Daftar pengguna berhasil diambil', 'data': [user.to_dict() for user in users]})

@app.route('/users', methods=['POST'])
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
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'pesan': 'Pengguna tidak ditemukan'}), 404
    return jsonify({'pesan': 'Detail pengguna berhasil diambil', 'data': user.to_dict()})

@app.route('/users/<int:user_id>', methods=['PUT'])
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
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'pesan': 'Pengguna tidak ditemukan'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'pesan': 'Pengguna berhasil dihapus'})

if __name__ == '__main__':
    app.run(debug=True)
