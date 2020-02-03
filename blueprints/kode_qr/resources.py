from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db, app, officer_required, payer_required, surveyor_required
from .model import *
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request
from blueprints.bukti_pembayaran.model import *
from blueprints.objek_pajak.model import *

blueprint_kode_qr = Blueprint("kode_QR", __name__)
api = Api(blueprint_kode_qr)

#resource model kode_qr oleh officer
class OfficerKodeQRResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
    
    #fungsi untuk mendapatkan data kode_qr berdasarkan idnya oleh officer
    @jwt_required
    @officer_required
    def get(self, id):
        kode_QR = KodeQR.query.get(id)
        if kode_QR is not None:
            return marshal(kode_QR, KodeQR.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status':'id not found'}, 404

    #fungsi untuk menambah row baru pada tabel kode_qr oleh officer
    @jwt_required
    @officer_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('bukti_pembayaran_id', location='json', required=True)
        args = parser.parse_args()

        bukti_pembayaran_id = args['bukti_pembayaran_id']
        bukti_pembayaran = BuktiPembayaran.query.get(bukti_pembayaran_id)
        if bukti_pembayaran is None:
            return {'status':'bukti_pembayaran_id not found'}, 404

        jumlah_kodeQR = bukti_pembayaran.jumlah_reklame
        nomor_sspd = bukti_pembayaran.nomor_sspd
        
        list_kode_QR = []
        for indeks in range(jumlah_kodeQR):
            kode_unik = "{nomor_sspd}{indeks}kodeunik".format(nomor_sspd=nomor_sspd, indeks=indeks)
            link_gambar = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={kode_unik}".format(kode_unik=kode_unik)
            kode_QR = KodeQR(bukti_pembayaran_id, kode_unik, link_gambar)
            db.session.add(kode_QR)
            db.session.commit()
            app.logger.debug('DEBUG : %s', kode_QR)
            list_kode_QR.append(marshal(kode_QR, KodeQR.response_fields))
        
        return list_kode_QR, 200, {'Content-Type': 'application/json'}

class OfficerKodeQRList(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
    @jwt_required
    @officer_required

    #fungsi untuk mendapatkan list kode_qr oleh officer
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('bukti_pembayaran_id', location='args', help='invalid filterby bukti_pembayaran_id')
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        kode_QR = KodeQR.query

        if args['bukti_pembayaran_id'] is not None:
            kode_QR = kode_QR.filter_by(bukti_pembayaran_id=args['bukti_pembayaran_id'])
        list_kode_QR = []
        for kode_QR_satuan in kode_QR.limit(args['rp']).offset(offset).all():
            list_kode_QR.append(marshal(kode_QR_satuan, KodeQR.response_fields))
        
        return list_kode_QR, 200, {'Content-Type': 'application/json'}

api.add_resource(OfficerKodeQRList, '/officer')
api.add_resource(OfficerKodeQRResource, '/officer', '/officer/<int:id>')