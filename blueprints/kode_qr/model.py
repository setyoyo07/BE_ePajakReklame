from blueprints import db
from flask_restful import fields
from datetime import datetime
from flask import Blueprint
from flask_restful import Api

blueprint_kode_qr = Blueprint("kode-qr", __name__)
api = Api(blueprint_kode_qr)

# model database kode QR
class KodeQR(db.Model):
    __tablename__ = "kode_QR"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bukti_pembayaran_id = db.Column(db.Integer, db.ForeignKey("bukti_pembayaran.id"))
    kode_unik = db.Column(db.String(255), default='')
    link_gambar = db.Column(db.String(1000), default='')
    status_scan = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "bukti_pembayaran_id": fields.Integer,
        "kode_unik": fields.String,
        "link_gambar": fields.String,
        "status_scan": fields.Boolean,
    }

    def __init__(self, bukti_pembayaran_id, kode_unik, link_gambar):
        self.bukti_pembayaran_id = bukti_pembayaran_id  
        self.kode_unik = kode_unik  
        self.link_gambar = link_gambar
        
    def __repr__(self):
        return "<KodeQR %r>" % self.id
