from blueprints import db
from flask_restful import fields
from datetime import datetime


class BuktiPembayaran(db.Model):
    __tablename__ = "buktipembayaran"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    laporan_id = db.Column(db.Integer, db.ForeignKey("laporan.id"))
    daerah_id = db.Column(db.Integer, db.ForeignKey("daerah.id"))
    nomor_sspd = db.Column(db.String(255), default='')
    status_buat_kode_qr = db.Column(db.Boolean, default=False)
    pelanggaran = db.Column(db.String(255), default='')
    jumlah_reklame = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "laporan_id": fields.Integer,
        "daerah_id": fields.Integer,
        "nomor_sspd": fields.String,
        "status_buat_kode_qr": fields.Boolean
        "pelanggaran": fields.String,
        "jumlah_reklame": fields.Integer,
    }

    def __init__(self, laporan_id, daerah_id, nomor_sspd, jumlah_reklame):
        self.laporan_id = laporan_id  
        self.daerah_id = daerah_id  
        self.nomor_sspd = nomor_sspd
        self.jumlah_reklame = jumlah_reklame  
        
    def __repr__(self):
        return "<BuktiPembayaran %r>" % self.id