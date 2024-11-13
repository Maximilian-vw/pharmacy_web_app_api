# config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Konfigurasi database MySQL dan JWT
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl:pwl123@localhost:3306/db_apotek_api'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskapi_usguessrun:b75649cf5f9200d1ea83d22591c4eb312c6a4f4b@styc1.h.filess.io:3305/flaskapi_usguessrun'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'WaHyUDi078'  # Key untuk JWT token

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Menjalankan app context
app.app_context().push()
