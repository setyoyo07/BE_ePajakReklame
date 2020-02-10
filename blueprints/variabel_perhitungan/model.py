from blueprints import db
from flask_restful import fields
from datetime import datetime
from flask import Blueprint
from flask_restful import Api

# Model database variabel perhitungan untuk keperluan perhitungan total biaya pajak
class VariabelPerhitungan(db.Model):
    __tablename__ = "variabel_perhitungan"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(255), default='')
    kata_kunci_induk = db.Column(db.String(255), default='')
    kata_kunci = db.Column(db.String(255), default='')
    nilai = db.Column(db.Float, default=0)
    status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "nama": fields.String,
        "kata_kunci_induk": fields.String,
        "kata_kunci": fields.String,
        "nilai": fields.Float,
        "status": fields.Boolean,
    }

    def __init__(self, nama, kata_kunci_induk, kata_kunci, nilai):
        self.nama = nama  
        self.kata_kunci_induk = kata_kunci_induk  
        self.kata_kunci = kata_kunci  
        self.nilai = nilai
        
    def __repr__(self):
        return "<VariabelPerhitungan %r>" % self.id
