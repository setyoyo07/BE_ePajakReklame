from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db, app, payer_required
from .model import *
from blueprints.payer.model import Payer
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request

blueprint_objek_pajak = Blueprint("objek_pajak", __name__)
api = Api(blueprint_objek_pajak)

#Resource model objek pajak oleh payer
class PayerObjekPajakResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200

    #fungsi untuk menambah data objek pajak baru oleh payer
    @jwt_required
    @payer_required
    def post(self):
        verify_jwt_in_request() 
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])

        parser = reqparse.RequestParser()
        parser.add_argument('nopd', location='json', required=True)
        parser.add_argument('nama_reklame', location='json', required=True)
        parser.add_argument('judul_reklame', location='json', required=True)
        parser.add_argument('tipe_reklame', location='json', required=True)
        parser.add_argument('jenis_reklame', location='json', required=True)
        parser.add_argument('foto', location='json', required=True)
        parser.add_argument('panjang', type=int, location='json', required=True)
        parser.add_argument('lebar', type=int, location='json', required=True)
        parser.add_argument('tinggi', type=int, location='json', required=True)
        parser.add_argument('jumlah', type=int, location='json', required=True)
        parser.add_argument('tanggal_pemasangan', location='json', required=True)
        parser.add_argument('tanggal_pembongakaran', location='json', required=True)
        parser.add_argument('masa_pajak', type=int, location='json', required=True)
        parser.add_argument('longitude', location='json', required=True)
        parser.add_argument('latitude', location='json', required=True)
        parser.add_argument('lokasi', location='json', required=True)
        args = parser.parse_args()

        objek_pajak = ObjekPajak(
            payer.id, 
            args["nopd"], 
            args["nama_reklame"],
            args["judul_reklame"], 
            args["tipe_reklame"], 
            args["jenis_reklame"],
            args["foto"], 
            args["panjang"], 
            args["lebar"], 
            args["tinggi"], 
            args["jumlah"],
            args["tanggal_pemasangan"],
            args["tanggal_pembongkaran"],
            args["masa_pajak"],
            args["longitude"],
            args["latitude"], 
            args["lokasi"]
            )
        db.session.add(objek_pajak)
        db.session.commit()
        app.logger.debug('DEBUG : %s', objek_pajak)
        
        return marshal(objek_pajak, ObjekPajak.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(PayerObjekPajakResource, '/payer')