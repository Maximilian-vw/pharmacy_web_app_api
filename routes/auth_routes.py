from flask import Blueprint, request
from controllers.auth_controller import register, login

auth_routes = Blueprint('auth', __name__)

auth_routes.route('/register', methods=['POST'])(register)
auth_routes.route('/login', methods=['POST'])(login)
