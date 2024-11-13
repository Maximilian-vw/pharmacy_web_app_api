# index.py
from config import app, db
from routes.auth_routes import auth_routes
from routes.obat_routes import obat_routes
from routes.transaksi_routes import transaksi_routes

# Daftarkan blueprint
app.register_blueprint(auth_routes)
app.register_blueprint(obat_routes)
app.register_blueprint(transaksi_routes)

# Route utama
@app.route('/', methods=['GET'])
def home():
    return 'HELLO WORLD'

#if __name__ == '__main__':
db.create_all()  # Membuat tabel jika belum ada
    #app.run(debug=True)
