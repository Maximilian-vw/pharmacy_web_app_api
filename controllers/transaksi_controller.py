from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from config import db
from models.transaksi import Transaksi
from models.pembeli import Pembeli

# Fungsi untuk membuat transaksi baru
@jwt_required()
def create_transaksi():
    """ Fungsi untuk membuat transaksi baru """
    # Ambil data dari body request
    data = request.get_json()

    # Pastikan ada data yang diperlukan
    if not data or not data.get('pembeli_id') or not data.get('obat_id') or not data.get('jumlah'):
        return jsonify({'message': 'Missing required fields'}), 400

    # Ambil ID pengguna yang sedang login (dari JWT)
    current_user_role = get_jwt_identity()  # ini adalah role dari pengguna
    current_user_id = Pembeli.query.filter_by(role=current_user_role).first().id

    # Pastikan hanya admin atau pemilik akun yang bisa membuat transaksi
    if data['pembeli_id'] != current_user_id and current_user_role != 'admin':
        return jsonify({'message': 'You can only make transactions for your own account!'}), 403

    # Jika admin, pastikan pembeli_id valid (ada dalam database)
    if current_user_role == 'admin':
        pembeli = Pembeli.query.get(data['pembeli_id'])
        if not pembeli:
            return jsonify({'message': 'Invalid pembeli ID'}), 404

    # Buat transaksi baru
    new_transaksi = Transaksi(
        pembeli_id=data['pembeli_id'],
        obat_id=data['obat_id'],
        jumlah=data['jumlah']
    )

    # Simpan transaksi ke database
    db.session.add(new_transaksi)
    db.session.commit()

    # Kembalikan response dengan data transaksi baru
    return jsonify({'message': 'Transaksi created successfully!', 'transaksi': new_transaksi.to_dict()}), 201

# Fungsi untuk mengambil semua transaksi
@jwt_required()
def get_transaksi():
    """ Fungsi untuk mengambil semua transaksi """
    transaksi_list = Transaksi.query.all()
    return jsonify([transaksi.to_dict() for transaksi in transaksi_list]), 200

# Fungsi untuk mengambil transaksi berdasarkan ID
@jwt_required()
def get_transaksi_by_id(id):
    """ Fungsi untuk mengambil transaksi berdasarkan ID """
    transaksi = Transaksi.query.get(id)
    if not transaksi:
        return jsonify({'message': 'Transaksi not found!'}), 404
    return jsonify(transaksi.to_dict()), 200

# Fungsi untuk memperbarui transaksi berdasarkan ID
@jwt_required()
def update_transaksi(id):
    """ Fungsi untuk memperbarui transaksi berdasarkan ID """
    # Ambil data dari body request
    data = request.get_json()

    # Cek apakah data lengkap
    if not data or not data.get('pembeli_id') or not data.get('obat_id') or not data.get('jumlah'):
        return jsonify({'message': 'Missing required fields'}), 400

    # Ambil transaksi berdasarkan id
    transaksi = Transaksi.query.get(id)
    if not transaksi:
        return jsonify({'message': 'Transaksi not found!'}), 404

    current_user_role = get_jwt_identity()  # role yang diambil dari token JWT
    current_user_id = Pembeli.query.filter_by(role=current_user_role).first().id

    # Pastikan hanya admin yang bisa memperbarui transaksi
    if current_user_role != 'admin':
        return jsonify({'message': 'Only admin can update transactions!'}), 403

    # Update transaksi dengan data baru
    transaksi.pembeli_id = data.get('pembeli_id', transaksi.pembeli_id)
    transaksi.obat_id = data.get('obat_id', transaksi.obat_id)
    transaksi.jumlah = data.get('jumlah', transaksi.jumlah)

    # Simpan perubahan ke database
    db.session.commit()

    return jsonify({'message': 'Transaksi updated successfully!', 'transaksi': transaksi.to_dict()}), 200

# Fungsi untuk menghapus transaksi berdasarkan ID
@jwt_required()
def delete_transaksi(id):
    """ Fungsi untuk menghapus transaksi berdasarkan ID """
    transaksi = Transaksi.query.get(id)
    if not transaksi:
        return jsonify({'message': 'Transaksi not found!'}), 404

    current_user_role = get_jwt_identity()  # role yang diambil dari token JWT

    # Pastikan hanya admin yang bisa menghapus transaksi
    if current_user_role != 'admin':
        return jsonify({'message': 'Only admin can delete transactions!'}), 403

    # Hapus transaksi dari database
    db.session.delete(transaksi)
    db.session.commit()

    return jsonify({'message': 'Transaksi deleted successfully!'}), 200
