from blueprints import db
from flask_restful import fields
from datetime import datetime
from flask import Blueprint
from flask_restful import Api

blueprint_variabel_perhitungan = Blueprint("variabel_perhitungan", __name__)
api = Api(blueprint_variabel_perhitungan)

# Model database variabel perhitungan untuk keperluan perhitungan total biaya pajak
class VariabelPerhitungan(db.Model):
    __tablename__ = "variabel_perhitungan"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tarif = db.Column(db.String(255), default='')
    tipe = db.Column(db.String(255), default='')
    biaya = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "tarif": fields.String,
        "tipe": fields.String,
        "biaya": fields.Integer,
    }

    def __init__(self, tarif, tipe, biaya):
        self.tarif = tarif  
        self.tipe = tipe  
        self.biaya = biaya
        
    def __repr__(self):
        return "<VariabelPerhitungan %r>" % self.id
