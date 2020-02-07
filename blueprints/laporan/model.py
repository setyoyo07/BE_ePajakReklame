from blueprints import db
from flask_restful import fields
from datetime import datetime

# Model database laporan pajak reklame
class Laporan(db.Model):
    __tablename__ = "laporan"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    objek_pajak_id = db.Column(db.Integer, db.ForeignKey("objek_pajak.id"))
    tarif_klasifikasi_jalan = db.Column(db.Integer, default=0)
    tarif_letak_pemasangan = db.Column(db.Integer, default=0)
    tarif_njopr = db.Column(db.Integer, default=0)
    tarif_tinggi_tanah = db.Column(db.Integer, default=0)
    total_pajak = db.Column(db.Integer, default=0)
    nomor_skpd = db.Column(db.String(255), default='')
    status_pembayaran = db.Column(db.Boolean, default=False)
    pembatalan_laporan = db.Column(db.Boolean, default=False)
    status_verifikasi = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "objek_pajak_id": fields.Integer,
        "tarif_klasifikasi_jalan": fields.Integer,
        "tarif_letak_pemasangan": fields.Integer,
        "tarif_njopr": fields.Integer,
        "tarif_tinggi_tanah": fields.Integer,
        "total_pajak": fields.Integer,
        "nomor_skpd": fields.String,
        "status_pembayaran": fields.Boolean,
        "pembatalan_laporan": fields.Boolean,
        "status_verifikasi": fields.Boolean
    }

    def __init__(self, objek_pajak_id, nomor_skpd):
        self.objek_pajak_id = objek_pajak_id 
        self.nomor_skpd = nomor_skpd
        
    def __repr__(self):
        return "<Laporan %r>" % self.id
