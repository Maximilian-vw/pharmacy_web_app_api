from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from config import db
from models.obat import Obat

def get_obat():
    obat_list = Obat.query.all()
    return jsonify([obat.to_dict() for obat in obat_list]), 200

def get_obat_by_id(obat_id):
    obat = Obat.query.get(obat_id)
    if not obat:
        return jsonify({'message': 'Obat not found!'}), 404
    return jsonify(obat.to_dict()), 200

@jwt_required()
def add_obat():
    user_role = get_jwt_identity() 
    if user_role != 'admin':
        return jsonify({'message': 'Admin privileges required!'}), 403 
    data = request.get_json() 

    if not data.get('nama') or not data.get('harga'):
        return jsonify({'message': 'Nama and harga are required!'}), 400
    new_obat = Obat(nama=data['nama'], harga=data['harga'])
    
    db.session.add(new_obat)
    db.session.commit()
    
    return jsonify({'message': 'Obat added successfully!', 'obat': new_obat.to_dict()}), 201

@jwt_required()
def update_obat(obat_id):
    user_role = get_jwt_identity()  
    if user_role != 'admin':
        return jsonify({'message': 'Admin privileges required!'}), 403  
    data = request.get_json()  
    
    obat = Obat.query.get(obat_id)
    if not obat:
        return jsonify({'message': 'Obat not found!'}), 404
    obat.nama = data.get('nama', obat.nama)  
    obat.harga = data.get('harga', obat.harga)  
    
    db.session.commit()
    return jsonify({'message': 'Obat updated successfully!', 'obat': obat.to_dict()}), 200


@jwt_required()
def delete_obat(obat_id):
    user_role = get_jwt_identity() 
    if user_role != 'admin':
        return jsonify({'message': 'Admin privileges required!'}), 403 
    obat = Obat.query.get(obat_id)
    if not obat:
        return jsonify({'message': 'Obat not found!'}), 404
    
    db.session.delete(obat)
    db.session.commit()
    return jsonify({'message': 'Obat deleted successfully!'}), 200
