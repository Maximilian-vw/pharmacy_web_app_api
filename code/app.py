import hashlib
from functools import wraps
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


# Initialize Flask app and config
app = Flask(__name__)

# Configuration for MySQL and Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl:pwl123@localhost:3306/db_apotek_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'WaHyUDi078'  # Key for JWT token

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Model Obat
class Obat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'harga': self.harga
        }

# Model Pembeli
class Pembeli(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')  # Default role 'user'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role  # Sertakan role dalam dictionary response
        }

# Model Transaksi
class Transaksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pembeli_id = db.Column(db.Integer, db.ForeignKey('pembeli.id'), nullable=False)
    obat_id = db.Column(db.Integer, db.ForeignKey('obat.id'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'pembeli_id': self.pembeli_id,
            'obat_id': self.obat_id,
            'jumlah': self.jumlah
        }

# Inisialisasi database (jalankan ini sekali untuk membuat tabel)
@app.before_request
def create_tables():
    db.create_all()

# Fungsi untuk menghasilkan MD5 hash dari password
def generate_md5_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

# Fungsi untuk memverifikasi password dengan MD5
def check_md5_password(stored_password, input_password):
    return stored_password == generate_md5_password(input_password)

# Fungsi untuk memverifikasi apakah pengguna adalah admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Ambil ID pengguna dari JWT
        user_id = get_jwt_identity()
        # Ambil data pengguna berdasarkan ID
        user = Pembeli.query.get(user_id)
        if user and user.role == 'admin':
            return fn(*args, **kwargs)
        else:
            return jsonify({"message": "Access forbidden: Admin only"}), 403
    return wrapper

#Tampilan Awal
@app.route('/')
def home():
    return 'HELLO WORLD'

# Endpoint untuk registrasi pembeli
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Cek apakah jwt_secret_key ada dan valid
    if data.get('jwt_secret_key') == app.config['JWT_SECRET_KEY']:
        role = 'admin'
    else:
        role = 'user'

    # Hash password menggunakan MD5
    hashed_password = generate_md5_password(data['password'])

    # Buat pengguna baru dengan role yang ditentukan
    new_user = Pembeli(username=data['username'], password=hashed_password, role=role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f'User registered successfully as {role}!'}), 201


# Endpoint untuk login dan mendapatkan token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Pembeli.query.filter_by(username=data['username']).first()

    if not user:
        return jsonify({'message': 'Invalid credentials!'}), 401

    # Bandingkan password yang dimasukkan dengan hash yang ada di database
    if not check_md5_password(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials!'}), 401

    # Jika password cocok, buat JWT access token
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

# Endpoint untuk mendapatkan semua obat
@app.route('/obat', methods=['GET'])
@jwt_required()
def get_obat():
    obat_list = Obat.query.all()
    return jsonify([obat.to_dict() for obat in obat_list]), 200

# Endpoint untuk mendapatkan detail obat berdasarkan ID
@app.route('/obat/<int:id>', methods=['GET'])
@jwt_required()
def get_obat_by_id(id):
    obat = Obat.query.get(id)
    if not obat:
        return jsonify({'message': 'Obat not found!'}), 404
    return jsonify(obat.to_dict()), 200

# Endpoint untuk menambahkan obat
@app.route('/obat', methods=['POST'])
@jwt_required()
@admin_required  # Hanya admin yang bisa mengakses
def add_obat():
    data = request.get_json()
    new_obat = Obat(nama=data['nama'], harga=data['harga'])
    db.session.add(new_obat)
    db.session.commit()
    return jsonify({'message': 'Obat added successfully!', 'obat': new_obat.to_dict()}), 201

# Endpoint untuk mengupdate obat (PUT)
@app.route('/obat/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required  # Hanya admin yang bisa mengakses
def update_obat(id):
    obat = Obat.query.get(id)
    if not obat:
        return jsonify({'message': 'Obat not found!'}), 404

    data = request.get_json()
    obat.nama = data.get('nama', obat.nama)
    obat.harga = data.get('harga', obat.harga)

    db.session.commit()
    return jsonify({'message': 'Obat updated successfully!', 'obat': obat.to_dict()}), 200

# Endpoint untuk melakukan update sebagian data obat (PATCH)
@app.route('/obat/<int:id>', methods=['PATCH'])
@jwt_required()
@admin_required  # Hanya admin yang bisa mengakses
def patch_obat(id):
    obat = Obat.query.get(id)
    if not obat:
        return jsonify({'message': 'Obat not found!'}), 404

    data = request.get_json()
    if 'nama' in data:
        obat.nama = data['nama']
    if 'harga' in data:
        obat.harga = data['harga']

    db.session.commit()
    return jsonify({'message': 'Obat partially updated successfully!', 'obat': obat.to_dict()}), 200

# Endpoint untuk menghapus obat
@app.route('/obat/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required  # Hanya admin yang bisa mengakses
def delete_obat(id):
    obat = Obat.query.get(id)
    if not obat:
        return jsonify({'message': 'Obat not found!'}), 404

    db.session.delete(obat)
    db.session.commit()
    return jsonify({'message': 'Obat deleted successfully!'}), 200

# Endpoint untuk membuat transaksi
@app.route('/transaksi', methods=['POST'])
@jwt_required()
def create_transaksi():
    data = request.get_json()

    # Ambil ID pengguna dari JWT token
    current_user_id = get_jwt_identity()

    # Cek apakah pembeli_id di request sesuai dengan ID pengguna saat ini
    if data['pembeli_id'] != current_user_id:
        return jsonify({'message': 'You can only make transactions for your own account!'}), 403

    # Buat transaksi baru
    new_transaksi = Transaksi(pembeli_id=data['pembeli_id'], obat_id=data['obat_id'], jumlah=data['jumlah'])
    db.session.add(new_transaksi)
    db.session.commit()

    return jsonify({'message': 'Transaksi created successfully!', 'transaksi': new_transaksi.to_dict()}), 201

# Endpoint untuk mendapatkan semua transaksi
@app.route('/transaksi', methods=['GET'])
@jwt_required()
def get_transaksi():
    transaksi_list = Transaksi.query.all()
    return jsonify([transaksi.to_dict() for transaksi in transaksi_list]), 200

# Endpoint untuk mendapatkan transaksi berdasarkan ID
@app.route('/transaksi/<int:id>', methods=['GET'])
@jwt_required()
def get_transaksi_by_id(id):
    transaksi = Transaksi.query.get(id)
    if not transaksi:
        return jsonify({'message': 'Transaksi not found!'}), 404
    return jsonify(transaksi.to_dict()), 200

# Endpoint untuk mengupdate transaksi (PUT) - Hanya admin yang bisa mengakses
@app.route('/transaksi/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required  # Hanya admin yang bisa mengakses
def update_transaksi(id):
    transaksi = Transaksi.query.get(id)
    if not transaksi:
        return jsonify({'message': 'Transaksi not found!'}), 404

    data = request.get_json()
    transaksi.pembeli_id = data.get('pembeli_id', transaksi.pembeli_id)
    transaksi.obat_id = data.get('obat_id', transaksi.obat_id)
    transaksi.jumlah = data.get('jumlah', transaksi.jumlah)

    db.session.commit()
    return jsonify({'message': 'Transaksi updated successfully!', 'transaksi': transaksi.to_dict()}), 200

@app.route('/transaksi/<int:id>', methods=['PATCH'])
@jwt_required()
@admin_required  # Hanya admin yang bisa mengakses
def patch_transaksi(id):
    transaksi = Transaksi.query.get(id)
    if not transaksi:
        return jsonify({'message': 'Transaksi not found!'}), 404

    data = request.get_json()
    if 'pembeli_id' in data:
        transaksi.pembeli_id = data['pembeli_id']
    if 'obat_id' in data:
        transaksi.obat_id = data['obat_id']
    if 'jumlah' in data:
        transaksi.jumlah = data['jumlah']

    db.session.commit()
    return jsonify({'message': 'Transaksi partially updated successfully!', 'transaksi': transaksi.to_dict()}), 200

# Endpoint untuk menghapus transaksi - Hanya admin yang bisa mengakses
@app.route('/transaksi/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required  # Hanya admin yang bisa mengakses
def delete_transaksi(id):
    transaksi = Transaksi.query.get(id)
    if not transaksi:
        return jsonify({'message': 'Transaksi not found!'}), 404

    db.session.delete(transaksi)
    db.session.commit()
    return jsonify({'message': 'Transaksi deleted successfully!'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
