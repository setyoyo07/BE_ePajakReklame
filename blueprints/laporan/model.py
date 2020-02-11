from blueprints import db
from flask_restful import fields
from datetime import datetime
from flask import Blueprint
from flask_restful import Api

blueprint_laporan = Blueprint("laporan", __name__)
api = Api(blueprint_laporan)

# Model database laporan pajak reklame
class Laporan(db.Model):
    __tablename__ = "laporan"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    objek_pajak_id = db.Column(db.Integer, db.ForeignKey("objek_pajak.id"))
    nfj = db.Column(db.Float, default=0) #nilai fungsi jalan
    nfr = db.Column(db.Float, default=0) #nilai fungsi ruang
    nsp = db.Column(db.Float, default=0) #nilai sudut pandang
    hdnspr = db.Column(db.Float, default=0) #harga dasar nilai strategis pajak reklame
    nkr = db.Column(db.Float, default=0) #nilai ketinggian reklame
    hdkr = db.Column(db.Float, default=0) #harga dasar ketinggian reklame
    nlr = db.Column(db.Float, default=0) #nilai luas reklame
    hdur = db.Column(db.Float, default=0) #harga dasar ukuran reklame
    njopr = db.Column(db.Float, default=0) #nilai jual objek pajak reklame
    nspr = db.Column(db.Float, default=0) #nilai strategis pemasangan reklame
    nsr = db.Column(db.Float, default=0) #nilai sewa reklame
    tarif_pajak = db.Column(db.Float, default=0)
    total_pajak = db.Column(db.Float, default=0)
    nomor_skpd = db.Column(db.String(255), default='')
    jumlah_termin = db.Column(db.Integer, default=0)
    tarif_termin = db.Column(db.Float, default=0)
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
        "nfj": fields.Float,
        "nfr": fields.Float,
        "nsp": fields.Float,
        "hdnspr": fields.Float,
        "nkr": fields.Float,
        "hdkr": fields.Float,
        "nlr": fields.Float,
        "hdur": fields.Float,
        "njopr": fields.Float,
        "nspr": fields.Float,
        "nsr": fields.Float,
        "tarif_pajak": fields.Float,
        "total_pajak": fields.Float,
        "jumlah_termin": fields.Integer,
        "tarif_termin": fields.Float,
        "nomor_skpd": fields.String,
        "status_pembayaran": fields.Boolean,
        "pembatalan_laporan": fields.Boolean,
        "status_verifikasi": fields.Boolean
    }

    def __init__(self, objek_pajak_id, nomor_skpd, nfj, nfr, nsp, hdnspr, nkr, hdkr, nlr, hdur,
                njopr, nspr, nsr, tarif_pajak, total_pajak, jumlah_termin):
        self.objek_pajak_id = objek_pajak_id 
        self.nomor_skpd = nomor_skpd
        self.nfj = nfj
        self.nfr = nfr
        self.nsp = nsp
        self.hdnspr = hdnspr
        self.nkr = nkr
        self.hdkr = hdkr
        self.nlr = nlr
        self.hdur = hdur
        self.njopr = njopr
        self.nspr = nspr
        self.nsr = nsr
        self.tarif_pajak = tarif_pajak
        self.total_pajak = total_pajak
        self.jumlah_termin = jumlah_termin
        
    def __repr__(self):
        return "<Laporan %r>" % self.id
