from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db, app, officer_required, payer_required, surveyor_required
from .model import *
from blueprints.payer.model import Payer
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request

blueprint_bukti_pembayaran = Blueprint("bukti_pembayaran", __name__)
api = Api(blueprint_bukti_pembayaran)

#Resource model bukti_pembayaran oleh officer
class OfficerBuktiPembayaranResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
    
    #fungsi untuk mendapatkan data bukti_pembayaran berdasarkan idnya oleh officer
    @jwt_required
    @officer_required
    def get(self, id):
        bukti_pembayaran = BuktiPembayaran.query.get(id)
        if bukti_pembayaran is not None:
            return marshal(bukti_pembayaran, BuktiPembayaran.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status':'id not found'}, 404

    #fungsi untuk menambah row baru pada data bukti_pembayaran oleh officer
    @jwt_required
    @officer_required
    def post(self):
        verify_jwt_in_request()
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        daerah_id_payer = payer.daerah_id

        parser = reqparse.RequestParser()
        parser.add_argument('nomor_sspd', location='json', required=True)
        parser.add_argument('jumlah_reklame', location='json', required=True)
        args = parser.parse_args()

        laporan_id = 1
        daerah_id = daerah_id_payer
        nomor_sspd = args['nomor_sspd']
        jumlah_reklame = args['jumlah_reklame']
        
        bukti_pembayaran = BuktiPembayaran(laporan_id, daerah_id, nomor_sspd, jumlah_reklame)
        db.session.add(bukti_pembayaran)
        db.session.commit()
        app.logger.debug('DEBUG : %s', bukti_pembayaran)
        
        return marshal(bukti_pembayaran, BuktiPembayaran.response_fields), 200, {'Content-Type': 'application/json'}

class OfficerBuktiPembayaranList(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
    
    #fungsi untuk mendapatkan data list bukti_pembayaran oleh officer
    @jwt_required
    @officer_required
    def get(self):
        verify_jwt_in_request()
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        daerah_id_payer = payer.daerah_id

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('laporan_id', location='args', help='invalid filterby laporan_id')
        parser.add_argument('nomor_sspd', location='args')
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        bukti_pembayaran = BuktiPembayaran.query

        if args['laporan_id'] is not None:
            bukti_pembayaran = bukti_pembayaran.filter_by(laporan_id=args['laporan_id'])
        if args['nomor_sspd'] is not None:
            bukti_pembayaran = bukti_pembayaran.filter(BuktiPembayaran.nomor_sspd.like('%' + args['nomor_sspd'] + '%'))

        list_bukti_pembayaran = []
        for bukti_pembayaran_satuan in bukti_pembayaran.limit(args['rp']).offset(offset).all():
            if bukti_pembayaran_satuan.daerah_id == daerah_id_payer:
                list_bukti_pembayaran.append(marshal(bukti_pembayaran_satuan, BuktiPembayaran.response_fields))
        
        return list_bukti_pembayaran, 200, {'Content-Type': 'application/json'}

api.add_resource(OfficerBuktiPembayaranList, '/officer')
api.add_resource(OfficerBuktiPembayaranResource, '/officer', '/officer/<int:id>')