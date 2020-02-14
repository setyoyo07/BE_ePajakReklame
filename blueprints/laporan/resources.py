from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db, app, payer_required, request
from .model import *
from sqlalchemy import desc
from blueprints.payer.model import Payer
from blueprints.objek_pajak.model import ObjekPajak
from blueprints.bukti_pembayaran.model import BuktiPembayaran
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request
import midtransclient

blueprint_laporan = Blueprint("laporan", __name__)
api = Api(blueprint_laporan)

#Resource model laporan oleh payer
class PayerLaporanList(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200

    #fungsi untuk mengambil data semua laporan milik payer
    @jwt_required
    @payer_required
    def get(self):
        verify_jwt_in_request() 
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        marshalPayer = marshal(payer, Payer.response_fields)
        laporan = Laporan.query
        laporan = laporan.order_by(desc(Laporan.id)).all()

        list_hasil = []
        for laporan_satuan in laporan:
            objek_pajak = ObjekPajak.query.get(laporan_satuan.objek_pajak_id)
            if objek_pajak.payer_id == payer.id :
                list_hasil.append({
                    "laporan":marshal(laporan_satuan, Laporan.response_fields),
                    "objek_pajak":marshal(objek_pajak, ObjekPajak.response_fields)
                })
        
        return {"list_laporan":list_hasil, "payer":marshalPayer}, 200, {'Content-Type': 'application/json'}

#Resource model laporan oleh payer untuk mendapat token midtrans
class PayerBayarLaporan(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200

    #fungsi untuk mengambil data token untuk pembayaran pajak di midtrans
    @jwt_required
    @payer_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('laporan_id', type=int, location='args', required=True)
        parser.add_argument('total_pajak', type=int, location='args', required=True)
        args = parser.parse_args()

        # initialize snap client object
        snap = midtransclient.Snap(
            is_production=False,
            server_key='SB-Mid-server-1tkGPlpmQKBQ8HC-iax-nI_U',
            client_key='SB-Mid-client-c-k-uXK4AgXKTYd2'
        )

        # prepare SNAP API parameter ( refer to: https://snap-docs.midtrans.com ) minimum parameter example
        param = {
            "transaction_details": {
                "order_id": args["laporan_id"],
                "gross_amount": args["total_pajak"]
            }
        }

        # create transaction
        transaction = snap.create_transaction(param)
        # transaction token
        transaction_token = transaction['token']
        # transaction redirect url
        transaction_redirect_url = transaction['redirect_url']

        return {"token":transaction_token, "url":transaction_redirect_url}, 200, {'Content-Type': 'application/json'}

    #fungsi callback status pembayaran pajak di midtrans
    def post(self):
         # initialize api client object
        api_client = midtransclient.CoreApi(
            is_production=False,
            server_key='SB-Mid-server-1tkGPlpmQKBQ8HC-iax-nI_U',
            client_key='SB-Mid-client-c-k-uXK4AgXKTYd2'
        )
        req_data = request.get_json()
        status_response = api_client.transactions.notification(req_data)

        order_id = status_response['order_id']
        transaction_status = status_response['transaction_status']
        fraud_status = status_response['fraud_status']
        status_code = status_response['status_code']

        if status_code == "200" :
            laporan = Laporan.query.get(order_id)
            laporan.status_pembayaran = True
            db.session.commit()

        return {'message':'status pembayaran diterima'},200
    
#Resource model laporan oleh payer spesifik berdasarkan laporan id-nya
class PayerLaporanResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200

    #fungsi untuk mengambil data laporan milik payer berdasarkan laporan id-nya
    @jwt_required
    @payer_required
    def get(self, id=None):
        verify_jwt_in_request() 
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        laporan = Laporan.query.get(id)

        if laporan is None:
            return {"message":"Data laporan tidak ditemukan"}, 404

        objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
        if objek_pajak.payer_id != payer.id : 
            return {"message":"Permission denied"}, 403

        marshalLaporan = marshal(laporan, Laporan.response_fields)
        marshalObjekPajak = marshal(objek_pajak, ObjekPajak.response_fields)
        
        return [{"laporan":marshalLaporan, "objek_pajak":marshalObjekPajak}], 200, {'Content-Type': 'application/json'}

    #fungsi untuk mengubah status pembatalan pada laporan milik user
    @jwt_required
    @payer_required
    def put(self):
        verify_jwt_in_request() 
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        parser = reqparse.RequestParser()
        parser.add_argument('laporan_id', type=int, location='json', required=True)
        parser.add_argument('status_pembayaran', type=bool, location='json')
        parser.add_argument('status_pembatalan', type=bool, location='json')
        args = parser.parse_args()
        laporan = Laporan.query.get(args['laporan_id'])

        if laporan is None:
            return {"message":"Data laporan tidam ditemukan"}, 404

        objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
        if objek_pajak.payer_id != payer.id : 
            return {"message":"Permission denied"}, 403
        if args['status_pembatalan'] is not None:
            laporan.pembatalan_laporan = True
            db.session.commit()
            return {"message": "Pembatalan Laporan sukses"}, 200, {'Content-Type': 'application/json'} 

        if args['status_pembayaran'] is not None:
            laporan.status_pembayaran = True
            db.session.commit()
            nomor_sspd = objek_pajak.nopd + laporan.nomor_skpd
            bukti_pembayaran = BuktiPembayaran(laporan.id, payer.daerah_id, nomor_sspd, objek_pajak.jumlah)
            db.session.add(bukti_pembayaran)
            db.session.commit()
            return {"message": "Pembayaran sukses",
            "laporan": marshal(laporan, Laporan.response_fields), 
            "bukti-pembayaran": marshal(bukti_pembayaran, BuktiPembayaran.response_fields)}, 200, {'Content-Type': 'application/json'}

api.add_resource(PayerLaporanList, '/payer')
api.add_resource(PayerLaporanResource, '/payer', '/payer/<int:id>')
api.add_resource(PayerBayarLaporan, '/payer/bayar')