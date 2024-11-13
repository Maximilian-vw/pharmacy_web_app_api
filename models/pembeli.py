# models/pembeli.py
from config import db

class Pembeli(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default="user")  # Menambahkan kolom role

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }
