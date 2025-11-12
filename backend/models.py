from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tipe_pengguna = db.Column(db.String(20), nullable=False)  # customer, driver, admin
    password = db.Column(db.String(200), nullable=False)  # hashed password

    def to_dict(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'email': self.email,
            'tipe_pengguna': self.tipe_pengguna
        }
