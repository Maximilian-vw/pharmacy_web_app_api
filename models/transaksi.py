# models/transaksi.py
from config import db

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
