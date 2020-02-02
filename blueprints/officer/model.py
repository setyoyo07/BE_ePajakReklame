from blueprints import db
from flask_restful import fields
from datetime import datetime

#model database officer
class Officer(db.Model):
    __tablename__ = "officer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nip = db.Column(db.String(255), unique=True, nullable=False)
    pin = db.Column(db.String(255), nullable=False)
    nama = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    daerah_id = db.Column(db.Integer, db.ForeignKey("daerah.id"))
    
    response_fields = {
        "id": fields.Integer,
        "nip": fields.String,
        "pin": fields.String,
        "nama": fields.String,
        "role": fields.String,
        "daerah_id": fields.Integer,
    }

    jwt_claim_fields = {
        "id": fields.Integer,
        "nip": fields.String,
        "nama": fields.String,
        "role": fields.String,
        "daerah_id": fields.Integer,
    }

    def __init__(self, nip, pin, nama, role, daerah_id):
        self.nip = nip
        self.pin = pin
        self.nama = nama
        self.role = role
        self.daerah_id = daerah_id

    def __repr__(self):
        return "<Officer %r>" % self.id
