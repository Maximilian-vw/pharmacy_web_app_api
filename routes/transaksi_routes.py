from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from controllers.transaksi_controller import create_transaksi, get_transaksi, get_transaksi_by_id, update_transaksi, delete_transaksi

transaksi_routes = Blueprint('transaksi', __name__)

# Menambahkan @jwt_required secara dinamis untuk semua rute
transaksi_routes.route('/transaksi', methods=['POST'])(jwt_required()(create_transaksi))
transaksi_routes.route('/transaksi', methods=['GET'])(jwt_required()(get_transaksi))
transaksi_routes.route('/transaksi/<int:id>', methods=['GET'])(jwt_required()(get_transaksi_by_id))
transaksi_routes.route('/transaksi/<int:id>', methods=['PUT'])(jwt_required()(update_transaksi))
transaksi_routes.route('/transaksi/<int:id>', methods=['DELETE'])(jwt_required()(delete_transaksi))
