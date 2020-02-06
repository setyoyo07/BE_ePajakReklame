from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db, app, officer_required, payer_required, surveyor_required
from .model import *
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request
from blueprints.bukti_pembayaran.model import *
from blueprints.laporan.model import *
from blueprints.objek_pajak.model import *
from blueprints.payer.model import Payer
import random

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
            return {'message':'bukti_pembayaran_id tidak ditemukan'}, 404
        if bukti_pembayaran.status_buat_kode_qr:
            return {'message':'kode QR sudah di generate'}
        jumlah_kodeQR = bukti_pembayaran.jumlah_reklame
        nomor_sspd = bukti_pembayaran.nomor_sspd
        
        list_kode_QR = []
        for indeks in range(jumlah_kodeQR):
            kode_unik = "alterratax{nomor_sspd}{indeks}".format(nomor_sspd=nomor_sspd, indeks=indeks)+"".join(random.choice(string.ascii_letters) for i in range(10))
            link_gambar = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={kode_unik}".format(kode_unik=kode_unik)
            kode_QR = KodeQR(bukti_pembayaran_id, kode_unik, link_gambar)
            db.session.add(kode_QR)
            db.session.commit()
            app.logger.debug('DEBUG : %s', kode_QR)
            list_kode_QR.append(marshal(kode_QR, KodeQR.response_fields))
        bukti_pembayaran.status_buat_kode_qr = True
        db.session.commit()

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
        parser.add_argument('kode_QR_id', location='args', help='invalid filterby kode_QR_id')
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        kode_QR = KodeQR.query

        if args['bukti_pembayaran_id'] is not None:
            kode_QR = kode_QR.filter_by(bukti_pembayaran_id=args['bukti_pembayaran_id'])
        
        if args['kode_QR_id'] is not None:
            kode_QR = kode_QR.filter(KodeQR.id.like('%' + args['kode_QR_id'] + '%'))

        list_kode_QR = []
        for kode_QR_satuan in kode_QR.limit(args['rp']).offset(offset).all():
            list_kode_QR.append(marshal(kode_QR_satuan, KodeQR.response_fields))

        bukti_pembayaran = BuktiPembayaran.query.get(args["bukti_pembayaran_id"])
        laporan = Laporan.query.get(bukti_pembayaran.laporan_id)
        objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
        return {"list_kode_qr": list_kode_QR, "nomor_sspd": bukti_pembayaran.nomor_sspd,
                "pelanggaran": bukti_pembayaran.pelanggaran,
                "nama_reklame": objek_pajak.nama_reklame}, 200, {'Content-Type': 'application/json'}

#resources model kodeQR untuk payer
class PayerKodeQRList(Resource):
  # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
      
    @jwt_required
    @payer_required
    #fungsi untuk mendapatkan list kode_qr oleh payer
    def get(self):
        verify_jwt_in_request()
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        id_payer = payer.id

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('bukti_pembayaran_id', location='args', help='invalid filterby bukti_pembayaran_id')
        parser.add_argument('kode_QR_id', location='args', help='invalid filterby kode_QR_id')
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        kode_QR = KodeQR.query

        if args['bukti_pembayaran_id'] is not None:
            kode_QR = kode_QR.filter_by(bukti_pembayaran_id=args['bukti_pembayaran_id'])
        if args['kode_QR_id'] is not None:
            kode_QR = kode_QR.filter(KodeQR.id.like('%' + args['kode_QR_id'] + '%'))

        list_kode_QR = []
        bukti_pembayaran = BuktiPembayaran.query.get(args["bukti_pembayaran_id"])
        laporan = Laporan.query.get(bukti_pembayaran.laporan_id)
        objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)

        for kode_QR_satuan in kode_QR.limit(args['rp']).offset(offset).all():
            if objek_pajak.payer_id == id_payer:
                list_kode_QR.append(marshal(kode_QR_satuan, KodeQR.response_fields))

        if objek_pajak.payer_id == id_payer:
            return {"list_kode_qr": list_kode_QR, "nomor_sspd": bukti_pembayaran.nomor_sspd,
                "pelanggaran": bukti_pembayaran.pelanggaran,
                "nama_reklame": objek_pajak.nama_reklame}, 200, {'Content-Type': 'application/json'}
        return {"status": "Bukti pembayaran tidak valid"}, 200, {'Content-Type': 'application/json'}

class PayerKodeQRResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
    
    #fungsi untuk mendapatkan data kode_qr berdasarkan idnya oleh payer
    @jwt_required
    @payer_required
    def get(self, id):
        kode_QR = KodeQR.query.get(id)
        if kode_QR is not None:
            return marshal(kode_QR, KodeQR.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status':'id not found'}, 404

    #fungsi untuk menambah row baru pada tabel kode_qr oleh payer
    @jwt_required
    @payer_required
    def post(self):
        verify_jwt_in_request()
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        id_payer = payer.id

        parser = reqparse.RequestParser()
        parser.add_argument('bukti_pembayaran_id', location='json', required=True)
        args = parser.parse_args()

        bukti_pembayaran_id = args['bukti_pembayaran_id']
        bukti_pembayaran = BuktiPembayaran.query.get(bukti_pembayaran_id)
        if bukti_pembayaran is None:
            return {'status':'bukti_pembayaran_id not found'}, 404
        laporan = Laporan.query.get(bukti_pembayaran.laporan_id)
        objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
        if objek_pajak.payer_id != id_payer:
            return {"status": "Bukti pembayaran tidak valid"}, 404, {'Content-Type': 'application/json'}
        if bukti_pembayaran.status_buat_kode_qr == True:
            return {"status": "Kode QR sudah di generate"}, 404, {'Content-Type': 'application/json'}
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
            
        bukti_pembayaran.status_buat_kode_qr = True
        db.session.commit()
        return list_kode_QR, 200, {'Content-Type': 'application/json'}

#resources model kodeQR untuk surveyor 
class SurveyorKodeQRResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
      
    #fungsi untuk mengubah status kode qr yang sudah discan
    @jwt_required
    @surveyor_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('kode_unik', type=str, location='json', default='')
        args = parser.parse_args()
        kode_QR = KodeQR.query.filter_by(kode_unik=args["kode_unik"]).first()
        if kode_QR is None:
            return {'message':'Kode QR tidak valid'}, 200, {'Content-Type': 'application/json'}
        if kode_QR.status_scan:
            return {'message':'Kode QR sudah terscan', "bukti_pembayaran_id":kode_QR.bukti_pembayaran_id}, 200, {'Content-Type': 'application/json'}
        kode_QR.status_scan = True
        db.session.commit()

        return {"bukti_pembayaran_id":kode_QR.bukti_pembayaran_id, "status_scan":kode_QR.status_scan}, 200, {'Content-Type': 'application/json'}

api.add_resource(OfficerKodeQRList, '/officer')
api.add_resource(OfficerKodeQRResource, '/officer', '/officer/<int:id>')
api.add_resource(SurveyorKodeQRResource, '/surveyor')
api.add_resource(PayerKodeQRList, '/payer')
api.add_resource(PayerKodeQRResource, '/payer', '/payer/<int:id>')
