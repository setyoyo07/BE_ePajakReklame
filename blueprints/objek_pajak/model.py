from blueprints import db
from flask_restful import fields
from datetime import datetime
from flask import Blueprint
from flask_restful import Api

#model database objek_pajak
class ObjekPajak(db.Model):
    __tablename__ = "objek_pajak"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payer_id = db.Column(db.Integer, db.ForeignKey("payer.id"))
    nopd = db.Column(db.String(255), nullable=False)
    nama_reklame = db.Column(db.String(255), nullable=False)
    judul_reklame = db.Column(db.String(255), nullable=False)
    tipe_reklame = db.Column(db.String(255), nullable=False)
    jenis_reklame = db.Column(db.String(255), nullable=False)
    foto = db.Column(db.String(1000), nullable=False)
    panjang = db.Column(db.Float, nullable=False)
    lebar = db.Column(db.Float, nullable=False)
    tinggi = db.Column(db.Float, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    tanggal_pemasangan = db.Column(db.DateTime)
    tanggal_pembongkaran = db.Column(db.DateTime)
    masa_pajak = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(255), nullable=False)
    lokasi = db.Column(db.String(255), nullable=False)
    muka = db.Column(db.Integer, nullable=False)
    luas = db.Column(db.Integer, nullable=False)
    tarif_tambahan = db.Column(db.String(255), nullable=False)
    letak_pemasangan = db.Column(db.String(255), nullable=False)
    klasifikasi_jalan = db.Column(db.String(255), nullable=False)
    sudut_pandang = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    response_fields = {
        "id": fields.Integer,
        "payer_id": fields.Integer,
        "nopd": fields.String,
        "nama_reklame": fields.String,
        "judul_reklame": fields.String,
        "tipe_reklame": fields.String,
        "jenis_reklame": fields.String,
        "foto": fields.String,
        "panjang": fields.Float,
        "tinggi": fields.Float,
        "lebar": fields.Float,
        "jumlah": fields.Integer,
        "tanggal_pemasangan": fields.DateTime,
        "tanggal_pembongkaran": fields.DateTime,
        "masa_pajak": fields.String,
        "longitude": fields.String,
        "latitude": fields.String,
        "lokasi": fields.String,
        "muka": fields.Integer,
        "luas": fields.Integer,
        "tarif_tambahan": fields.String,
        "letak_pemasangan": fields.String,
        "klasifikasi_jalan": fields.String,
        "sudut_pandang": fields.String,
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
    }

    def __init__(self, payer_id, nopd, nama_reklame, judul_reklame, tipe_reklame, jenis_reklame,
                foto, panjang, lebar, tinggi, jumlah, tanggal_pemasangan, tanggal_pembongkaran, masa_pajak,
                longitude, latitude, lokasi, muka, luas, tarif_tambahan, letak_pemasangan, klasifikasi_jalan,
                sudut_pandang):
        self.payer_id = payer_id
        self.nopd = nopd
        self.nama_reklame = nama_reklame
        self.judul_reklame = judul_reklame
        self.tipe_reklame = tipe_reklame
        self.jenis_reklame = jenis_reklame
        self.foto = foto
        self.panjang = panjang
        self.tinggi = tinggi
        self.lebar = lebar
        self.jumlah = jumlah
        self.tanggal_pemasangan = tanggal_pemasangan
        self.tanggal_pembongkaran = tanggal_pembongkaran
        self.masa_pajak = masa_pajak
        self.longitude = longitude
        self.latitude = latitude
        self.lokasi = lokasi
        self.muka = muka
        self.luas = luas
        self.tarif_tambahan = tarif_tambahan
        self.letak_pemasangan = letak_pemasangan
        self.klasifikasi_jalan = klasifikasi_jalan
        self.sudut_pandang = sudut_pandang
        
    def __repr__(self):
        return "<ObjekPajak %r>" % self.id
