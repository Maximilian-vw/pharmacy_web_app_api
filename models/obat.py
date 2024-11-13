# models/obat.py
from config import db

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
