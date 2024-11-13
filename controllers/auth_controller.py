from flask import jsonify, request, current_app
from werkzeug.security import check_password_hash
import hashlib
from models.pembeli import Pembeli
from config import db
from flask_jwt_extended import create_access_token, jwt_required

def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required!'}), 400

    user = Pembeli.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'message': 'User already exists!'}), 409

    hashed_password = hashlib.md5(data['password'].encode()).hexdigest()
    role = "admin" if data.get("jwt_secret_key") == current_app.config['JWT_SECRET_KEY'] else "user"
    new_user = Pembeli(username=data['username'], password=hashed_password, role=role)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=role)  
    if role == "admin":
        return jsonify({'message': 'User registered successfully as Admin!',
                        'access_token': access_token}), 201
    else:
        return jsonify({'message': 'User registered successfully!',
                        'access_token': access_token}), 201


def login():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required!'}), 400

    user = Pembeli.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'message': 'Invalid credentials!'}), 401

    hashed_input_password = hashlib.md5(data['password'].encode()).hexdigest()
    if hashed_input_password != user.password:
        return jsonify({'message': 'Invalid credentials!'}), 401
    access_token = create_access_token(identity=user.role)

    return jsonify({
        'message': 'Login successful!',
        'access_token': access_token
    }), 200
