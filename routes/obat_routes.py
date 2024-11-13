from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from controllers.obat_controller import get_obat, get_obat_by_id, add_obat, update_obat, delete_obat

obat_routes = Blueprint('obat_routes', __name__)

# Menambahkan @jwt_required secara dinamis untuk semua rute yang memerlukan autentikasi
obat_routes.route('/obat', methods=['GET'])(get_obat)
obat_routes.route('/obat/<int:obat_id>', methods=['GET'])(get_obat_by_id)

# Pastikan rute POST, PUT, DELETE hanya dapat diakses oleh pengguna yang terautentikasi (admin)
obat_routes.route('/obat', methods=['POST'])(jwt_required()(add_obat))
obat_routes.route('/obat/<int:obat_id>', methods=['PUT'])(jwt_required()(update_obat))
obat_routes.route('/obat/<int:obat_id>', methods=['DELETE'])(jwt_required()(delete_obat))
