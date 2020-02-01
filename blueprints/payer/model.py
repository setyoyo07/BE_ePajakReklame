from blueprints import db
from flask_restful import fields
from datetime import datetime

#model database payer
class Payer(db.Model):
    __tablename__ = "payer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    npwpd = db.Column(db.String(255), unique=True, nullable=False)
    pin = db.Column(db.String(255), nullable=False)
    nama = db.Column(db.String(255), nullable=False)
    daerah_id = db.Column(db.Integer, db.ForeignKey("daerah.id"))
    objek_pajak = db.relationship('ObjekPajak', cascade="all,delete", backref='payer', lazy=True)
    
    response_fields = {
        "id": fields.Integer,
        "npwpd": fields.String,
        "pin": fields.String,
        "nama": fields.String,
        "daerah_id": fields.Integer,
    }

    jwt_claim_fields = {
        "id": fields.Integer,
        "npwpd": fields.String,
        "nama": fields.String,
        "role": fields.String,
        "daerah_id": fields.Integer,
    }

    def __init__(self, npwpd, pin, nama, daerah_id):
        self.npwpd = npwpd
        self.pin = pin
        self.nama = nama
        self.daerah_id = daerah_id

    def __repr__(self):
        return "<Payer %r>" % self.id
