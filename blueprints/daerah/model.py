from blueprints import db
from flask_restful import fields
from datetime import datetime
from flask import Blueprint
from flask_restful import Api

blueprint_daerah = Blueprint("daerah", __name__)
api = Api(blueprint_daerah)

class Daerah(db.Model):
    __tablename__ = "daerah"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(255), unique=True, nullable=False)
    officer = db.relationship('Officer', cascade="all,delete", backref='daerah', lazy=True)
    payer = db.relationship('Payer', cascade="all,delete", backref='daerah', lazy=True)
    
    response_fields = {
        "id": fields.Integer,
        "nama": fields.String,
    }

    def __init__(self, nama):
        self.nama = nama

    def __repr__(self):
        return "<Daerah %r>" % self.id