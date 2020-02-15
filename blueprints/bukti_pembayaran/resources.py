from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db, app, officer_required, payer_required, surveyor_required
from .model import *
from sqlalchemy import desc
from blueprints.officer.model import Officer
from blueprints.laporan.model import Laporan
from blueprints.objek_pajak.model import ObjekPajak
from blueprints.payer.model import Payer
from blueprints.kode_qr.model import KodeQR
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request

blueprint_bukti_pembayaran = Blueprint("bukti_pembayaran", __name__)
api = Api(blueprint_bukti_pembayaran)

#Resource model bukti_pembayaran oleh officer
class OfficerBuktiPembayaranResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200

    #fungsi untuk menambah row baru pada data bukti_pembayaran oleh officer
    @jwt_required
    @officer_required
    def post(self):
        verify_jwt_in_request()
        officer_claims_data = get_jwt_claims()
        officer = Officer.query.get(officer_claims_data["id"])
        daerah_id_officer = officer.daerah_id

        parser = reqparse.RequestParser()
        parser.add_argument('nomor_sspd', type=str, location='json', required=True)
        parser.add_argument('jumlah_reklame', type=int, location='json', required=True)
        args = parser.parse_args()

        laporan_id = 1
        daerah_id = daerah_id_officer
        nomor_sspd = args['nomor_sspd']
        jumlah_reklame = args['jumlah_reklame']

        if jumlah_reklame < 1:
            return {"message":"Jumlah reklame minimal 1"}, 400

        cek_bukti_pembayaran = BuktiPembayaran.query.filter_by(nomor_sspd=nomor_sspd).first()
        if cek_bukti_pembayaran is not None:
            return {"message":"Nomor SSPD sudah terdaftar"}, 400
        else:       
            bukti_pembayaran = BuktiPembayaran(laporan_id, daerah_id, nomor_sspd, jumlah_reklame)
            db.session.add(bukti_pembayaran)
            db.session.commit()
            app.logger.debug('DEBUG : %s', bukti_pembayaran)
            
            return marshal(bukti_pembayaran, BuktiPembayaran.response_fields), 200, {'Content-Type': 'application/json'}

    #fungsi untuk mendapatkan data list bukti_pembayaran oleh officer
    @jwt_required
    @officer_required
    def get(self):
        verify_jwt_in_request()
        officer_claims_data = get_jwt_claims()
        officer = Officer.query.get(officer_claims_data["id"])
        daerah_id_officer = officer.daerah_id

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('nomor_sspd', location='args')
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        bukti_pembayaran = BuktiPembayaran.query

        page = args["p"]
        row_page = args["rp"]

        if args['nomor_sspd'] is not None:
            bukti_pembayaran = bukti_pembayaran.filter(BuktiPembayaran.nomor_sspd.like('%' + args['nomor_sspd'] + '%'))

        bukti_pembayaran = bukti_pembayaran.order_by(desc(BuktiPembayaran.id))
        list_bukti_pembayaran = []
        for bukti_pembayaran_satuan in bukti_pembayaran.limit(args['rp']).offset(offset).all():
            if bukti_pembayaran_satuan.daerah_id == daerah_id_officer:
                laporan = Laporan.query.get(bukti_pembayaran_satuan.laporan_id)
                objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
                kode_QR = KodeQR.query.filter_by(bukti_pembayaran_id=bukti_pembayaran_satuan.id)
                kode_QR_scan = 0
                for kode_QR_satuan in kode_QR.all():
                    if kode_QR_satuan.status_scan == True:
                        kode_QR_scan+=1
                payer = Payer.query.get(objek_pajak.payer_id)
                list_bukti_pembayaran.append({"bukti_pembayaran":marshal(bukti_pembayaran_satuan, BuktiPembayaran.response_fields),
                                    "objek_pajak":marshal(objek_pajak, ObjekPajak.response_fields),
                                    "payer":payer.nama,
                                    "kode_QR terscan": kode_QR_scan})

        list_semua_bukti_pembayaran = []
        for bukti_pembayaran_satuan in bukti_pembayaran.all():
            if bukti_pembayaran_satuan.daerah_id == daerah_id_officer:
                laporan = Laporan.query.get(bukti_pembayaran_satuan.laporan_id)
                objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
                kode_QR = KodeQR.query.filter_by(bukti_pembayaran_id=bukti_pembayaran_satuan.id)
                kode_QR_scan = 0
                for kode_QR_satuan in kode_QR.all():
                    if kode_QR_satuan.status_scan == True:
                        kode_QR_scan+=1
                payer = Payer.query.get(objek_pajak.payer_id)
                list_semua_bukti_pembayaran.append({"bukti_pembayaran":marshal(bukti_pembayaran_satuan, BuktiPembayaran.response_fields),
                                    "objek_pajak":marshal(objek_pajak, ObjekPajak.response_fields),
                                    "payer":payer.nama,
                                    "kode_QR terscan": kode_QR_scan})
        jumlah_bukti_pembayaran = len(list_semua_bukti_pembayaran)
        maks_page = 1 + ((jumlah_bukti_pembayaran-1) // row_page)

        return {"page":page, "row_page":row_page, "maks_page":maks_page,
            "list_bukti_pembayaran":list_bukti_pembayaran}, 200, {'Content-Type': 'application/json'}

# class model bukti pembayaran untuk payer
class PayerBuktiPembayaranResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
    
    #fungsi untuk mendapatkan data bukti_pembayaran oleh payer berdasarkan id-nya
    @jwt_required
    @payer_required
    def get(self, id=None):
        verify_jwt_in_request()
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        bukti_pembayaran = BuktiPembayaran.query.filter_by(laporan_id=id).first()
        if bukti_pembayaran is None:
            return {"message":"Data bukti pembayaran tidak ditemukan"}, 404

        laporan = Laporan.query.get(bukti_pembayaran.laporan_id)
        objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
        if objek_pajak.payer_id != payer.id :
            return {"message":"Permission denied"}, 403

        hasil = {
            "bukti_pembayaran": marshal(bukti_pembayaran, BuktiPembayaran.response_fields),
            "objek_pajak": marshal(objek_pajak, ObjekPajak.response_fields),
            "laporan": marshal(laporan, Laporan.response_fields),
            "payer": marshal(payer, Payer.response_fields)
        }
        
        return hasil, 200, {'Content-Type': 'application/json'}

# Resources model BuktiPembayaran untuk Surveyor
class SurveyorBuktiPembayaranList(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200

    #fungsi untuk mendapatkan data list bukti_pembayaran, lokasi reklame, status scan
    @jwt_required
    @surveyor_required
    def get(self):
        verify_jwt_in_request()
        officer_claims_data = get_jwt_claims()
        daerah_id_officer = officer_claims_data["daerah_id"]
        bukti_pembayaran = BuktiPembayaran.query
        bukti_pembayaran = bukti_pembayaran.filter_by(status_buat_kode_qr=True).all()
        list_result = []
        for bukti_pembayaran_satuan in bukti_pembayaran:
            if bukti_pembayaran_satuan.daerah_id == daerah_id_officer:
                if bukti_pembayaran_satuan.laporan_id != 1:
                    laporan = Laporan.query.get(bukti_pembayaran_satuan.laporan_id)
                    objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
                    kode_QR = KodeQR.query.filter_by(bukti_pembayaran_id=bukti_pembayaran_satuan.id)
                    kode_QR_scan = 0
                    for kode_QR_satuan in kode_QR.all():
                        if kode_QR_satuan.status_scan == True:
                            kode_QR_scan+=1
                    if kode_QR_scan == 0:
                        status_scan = "Belum Valid"
                    elif kode_QR_scan == bukti_pembayaran_satuan.jumlah_reklame:
                        status_scan = "Sudah Valid"
                    else :
                        status_scan = "Menuju Valid"
                    list_result.append({"bukti_pembayaran":marshal(bukti_pembayaran_satuan, BuktiPembayaran.response_fields),
                                        "objek_pajak":marshal(objek_pajak, ObjekPajak.response_fields),
                                        "status_scan": status_scan,
                                        "kodeQR_terscan": kode_QR_scan})
        
        return list_result, 200, {'Content-Type': 'application/json'}

# Resources model BuktiPembayaran untuk Surveyor spesifik by ID
class SurveyorBuktiPembayaranResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200
    
    #fungsi untuk mendapatkan data detail bukti_pembayaran dan objek pajak
    @jwt_required
    @surveyor_required
    def get(self, id=None):
        verify_jwt_in_request()
        officer_claims_data = get_jwt_claims()
        officer = Officer.query.get(officer_claims_data["id"])
        daerah_id_officer = officer.daerah_id

        bukti_pembayaran = BuktiPembayaran.query.get(id)
        if bukti_pembayaran.daerah_id == daerah_id_officer:
            laporan = Laporan.query.get(bukti_pembayaran.laporan_id)
            objek_pajak = ObjekPajak.query.get(laporan.objek_pajak_id)
            kode_QR = KodeQR.query.filter_by(bukti_pembayaran_id=bukti_pembayaran.id)
            kode_QR_scan = 0
            for kode_QR_satuan in kode_QR.all():
                if kode_QR_satuan.status_scan == True:
                    kode_QR_scan+=1
            result = {"bukti_pembayaran":marshal(bukti_pembayaran, BuktiPembayaran.response_fields),
                    "objek_pajak":marshal(objek_pajak, ObjekPajak.response_fields),
                    "kode_QR_terscan": kode_QR_scan}
        
        return result, 200, {'Content-Type': 'application/json'}

    #fungsi untuk mengubah data pelanggaran pajak reklame oleh surveyor
    @jwt_required
    @surveyor_required
    def put(self):
        verify_jwt_in_request()
        officer_claims_data = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument("bukti_pembayaran_id",type=int, location="json")
        parser.add_argument("pelanggaran", location="json")
        args = parser.parse_args()
        bukti_pembayaran = BuktiPembayaran.query.get(args["bukti_pembayaran_id"])
        if bukti_pembayaran is None:
            return {'message':'Data Not Found'}, 404
        if args["pelanggaran"] is not None:
            bukti_pembayaran.pelanggaran = args["pelanggaran"] + " (Surveyor: " + officer_claims_data["nama"] + ")"
            db.session.commit()
            return marshal(bukti_pembayaran, BuktiPembayaran.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(SurveyorBuktiPembayaranList, '/surveyor')
api.add_resource(SurveyorBuktiPembayaranResource, '/surveyor', '/surveyor/<int:id>')
api.add_resource(OfficerBuktiPembayaranResource, '/officer', '/officer/<int:id>')
api.add_resource(PayerBuktiPembayaranResource, '/payer/<int:id>')