from flask import Blueprint, request, jsonify
from .. import db
from ..models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not all([username, password, role]) or role not in ['merchant', 'user']:
        return jsonify({"error": "Invalid input"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username exists"}), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
