from flask_login import login_required, current_user
from flask import jsonify, session
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({'pesan': 'Akses ditolak. Hanya admin yang diizinkan.'}), 403
        return f(*args, **kwargs)
    return decorated_function

def login_required_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'pesan': 'Login diperlukan.'}), 401
        return f(*args, **kwargs)
    return decorated_function
